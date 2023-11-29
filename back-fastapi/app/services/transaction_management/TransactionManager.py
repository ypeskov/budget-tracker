from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from icecream import ic

from app.logger_config import logger

from app.models.Currency import Currency
from app.models.Transaction import Transaction
from app.models.Account import Account
from app.models.UserCategory import UserCategory

from app.schemas.transaction_schema import UpdateTransactionSchema
from app.services.CurrencyProcessor import CurrencyProcessor

ic.configureOutput(includeContext=True)


def check_account_ownership(user_id: int, account_id: int, db: Session):
    """ Check if account belongs to user """
    if account_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Account id is required')

    account: Account = db.query(Account).filter_by(id=account_id).one_or_none()  # type: ignore
    if account is None:
        logger.error(f'Account {account_id} not found')
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Account not found')

    if account.user_id != user_id:
        logger.error(
            f'User {user_id} tried to create transaction with not own account {account_id}')
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Forbidden')

    return True


class TransactionManager:
    def __init__(self, transaction_details: UpdateTransactionSchema, user_id: int, db: Session):
        self._db = db
        self._transaction_details = transaction_details
        self._user_id = user_id
        self._is_update = False
        self._prev_amount = Decimal(0.0)
        self._prev_target_account_id = None
        self._prev_target_amount = Decimal(0.0)
        self._prev_is_transfer = None
        self._prev_is_income = None

        self._prepare_transaction()
        self.set_account(transaction_details.account_id)
        self.set_currency()
        self.set_date_time(transaction_details.date_time)

        self._transaction.amount = transaction_details.amount
        self._transaction.label = transaction_details.label
        self._transaction.notes = transaction_details.notes

        if transaction_details.is_transfer is True:
            self.set_account(transaction_details.target_account_id, 'target_')
            self._transaction.is_transfer = True
            self._transaction.exchange_rate = transaction_details.exchange_rate
            self._transaction.target_amount = transaction_details.target_amount
            self._transaction.category_id = None
        else:
            self._transaction.is_transfer = False
            self._transaction.category_id = transaction_details.category_id
            self._transaction.is_income = transaction_details.is_income

    def set_date_time(self, date_time: datetime | None = None) -> 'TransactionManager':
        if self._transaction.date_time is None:
            self._transaction.date_time = datetime.now(timezone.utc)
        else:
            self._transaction.date_time = date_time

        return self

    def set_currency(self, currency_id: int = None) -> 'TransactionManager':
        if currency_id is None:
            currency_id = self._transaction_details.currency_id
        if currency_id is None:
            account: Account = self._db.query(Account).filter_by(  # type: ignore
                id=self._transaction_details.account_id).one_or_none()
            if account is None:
                logger.error(f'Account {self._transaction_details.account_id} not found')
                raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Account not found')
            currency_id = account.currency_id

        currency: Currency = self._db.query(Currency).filter_by(id=currency_id).one_or_none()  # type: ignore
        if currency is None:
            logger.error(f'Currency {currency_id} not found')
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Currency not found')

        self._transaction.currency_id = currency.id
        self._transaction.currency = currency

        return self

    def set_account(self, account_id: int | None = None, account_prefix: str = '') -> 'TransactionManager':
        try:
            check_account_ownership(self._transaction.user_id, account_id, self._db)
            setattr(self._transaction, f'{account_prefix}account_id', account_id)
            account: Account = self._db.query(Account).filter_by(id=account_id).one_or_none()  # type: ignore
            setattr(self._transaction, f'{account_prefix}account', account)
        except HTTPException as e:
            logger.error(f'Error checking account ownership: {e.detail}')
            raise e
        return self

    def _prepare_transaction(self) -> 'TransactionManager':
        """ Prepare transaction object for update or create."""
        if self._transaction_details.id is not None:
            self._transaction: Transaction = self._db.query(Transaction).filter_by(  # type: ignore
                id=self._transaction_details.id).one_or_none()

            if self._transaction is None:
                logger.error(f'Transaction {self._transaction_details.id} not found')
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    detail=f'Transaction {self._transaction_details.id} not found')

            if self._user_id != self._transaction.user_id:
                logger.error(
                    f'User {self._user_id} tried to update transaction {self._transaction.id} of user {self._transaction.user_id}')
                raise HTTPException(status.HTTP_403_FORBIDDEN, 'Forbidden')

            self._is_update = True
            self._prev_amount = self._transaction.amount
            self._prev_target_account_id = self._transaction.target_account_id
            self._prev_target_amount = self._transaction.target_amount
            self._prev_is_transfer = self._transaction.is_transfer
            self._prev_is_income = self._transaction.is_income
        else:
            self._is_update = False
            self._prev_amount = Decimal(0.0)
            self._prev_target_amount = Decimal(0.0)
            self._transaction: Transaction = Transaction()
            self._transaction.user_id = self._user_id
        return self

    def get_transaction(self) -> Transaction:
        return self._transaction

    def process(self) -> 'TransactionManager':
        if self._transaction.is_transfer:
            self._process_transfer_type()
        else:
            self._process_non_transfer_type()

        self._db.add(self._transaction)
        self._db.commit()
        self._db.refresh(self._transaction)

        return self

    def _process_transfer_type(self) -> None:
        """This function processes case of transfer from one account to another"""

        if self._transaction.account.currency_id != self._transaction.target_account.currency_id:
            currency_processor: CurrencyProcessor = CurrencyProcessor(self._transaction, self._db)
            transaction = currency_processor.calculate_exchange_rate()
        else:
            self._transaction.target_amount = self._transaction.amount

        self._transaction.account.balance -= self._transaction.amount
        self._transaction.target_account.balance += self._transaction.target_amount

    def _process_non_transfer_type(self):
        """If the transaction is not transfer from one account to another then this function processes it"""

        try:
            category = self._db.query(UserCategory).filter_by(id=self._transaction.category_id).one()
        except NoResultFound:
            logger.error(f'Invalid category {self._transaction.category_id}')
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid category')

        if category.user_id != self._user_id:
            logger.error(f'User {self._user_id} tried to update transaction {self._transaction.id} ' +
                         f'with not own category {self._transaction.category_id}')
            raise HTTPException(status.HTTP_403_FORBIDDEN, 'Forbidden')

        if self._is_update:
            if self._prev_is_income:
                self._transaction.account.balance -= self._prev_amount
            else:
                self._transaction.account.balance += self._prev_amount

        if self._transaction.is_income:
            self._transaction.account.balance += self._transaction.amount
        else:
            self._transaction.account.balance -= self._transaction.amount
