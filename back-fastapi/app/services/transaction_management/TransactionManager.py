from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from icecream import ic

from app.logger_config import logger

from app.models.Currency import Currency
from app.models.Transaction import Transaction
from app.models.Account import Account
from app.models.UserCategory import UserCategory
from app.services.errors import AccessDenied, InvalidCategory, InvalidAccount, InvalidCurrency
from app.services.transaction_management.errors import InvalidTransaction
from app.schemas.transaction_schema import UpdateTransactionSchema, CreateTransactionSchema
from app.services.CurrencyProcessor import CurrencyProcessor

ic.configureOutput(includeContext=True)


class TransactionState(BaseModel):
    user_id: int
    db: Session
    transaction_details: UpdateTransactionSchema | CreateTransactionSchema
    is_update: bool = False
    prev_account_id: int | None = None
    prev_account: Account | None = None
    prev_new_balance: Decimal = Decimal(0.0)
    prev_amount: Decimal = Decimal(0.0)
    prev_target_account_id: int | None = None
    prev_target_new_balance: Decimal = Decimal(0.0)
    prev_target_amount: Decimal = Decimal(0.0)
    prev_is_transfer: bool = False
    prev_is_income: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)


def check_account_ownership(user_id: int, account_id: int | None, db: Session):
    """ Check if account belongs to user """
    if account_id is None:
        raise InvalidAccount()

    account: Account = db.query(Account).filter_by(id=account_id).one_or_none()  # type: ignore
    if account is None:
        logger.error(f'Account {account_id} not found')
        raise InvalidAccount()

    if account.user_id != user_id:
        logger.error(
            f'User {user_id} tried to create transaction with not own account {account_id}')
        raise AccessDenied()

    return True


class TransactionManager:
    def __init__(self,
                 transaction_details: UpdateTransactionSchema | CreateTransactionSchema,
                 user_id: int,
                 db: Session):
        self.state = TransactionState(user_id=user_id, db=db, transaction_details=transaction_details)
        self._transaction: Transaction = Transaction()
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
            self._transaction.target_amount = transaction_details.target_amount  # type: ignore
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

    def set_currency(self, currency_id: int | None = None) -> 'TransactionManager':
        if currency_id is None:
            currency_id = self.state.transaction_details.currency_id

        if currency_id is None:
            account = self.state.db.query(Account).filter_by(id=self.state.transaction_details.account_id).one_or_none()
            if account is None:
                logger.error(f'Account {self.state.transaction_details.account_id} not found')
                raise InvalidAccount()
            currency_id = account.currency_id

        currency = self.state.db.query(Currency).filter_by(id=currency_id).one_or_none()
        if currency is None:
            logger.error(f'Currency {currency_id} not found')
            raise InvalidCurrency()

        self._transaction.currency_id = currency.id
        self._transaction.currency = currency

        return self

    def set_account(self, account_id: int | None = None, account_prefix: str = '') -> 'TransactionManager':
        try:
            check_account_ownership(self.state.user_id, account_id, self.state.db)
            setattr(self._transaction, f'{account_prefix}account_id', account_id)
            account = self.state.db.query(Account).filter_by(id=account_id).one_or_none()
            setattr(self._transaction, f'{account_prefix}account', account)
        except AccessDenied as e:
            logger.error(f'Access denied. user_id={self.state.user_id}, account_id={account_id}')
            raise e
        return self

    def _prepare_transaction(self):
        transaction_details = self.state.transaction_details

        if transaction_details.id is not None:
            self._transaction = self.state.db.query(Transaction).filter_by(
                id=transaction_details.id).one_or_none()  # type: ignore

            if self._transaction is None:
                logger.error(f'Transaction {transaction_details.id} not found')
                raise InvalidTransaction(detail=f'Transaction {transaction_details.id} not found')

            if self.state.user_id != self._transaction.user_id:
                logger.error(
                    f'User {self.state.user_id} tried to update self._transaction {self._transaction.id} of user '
                    + f'{self._transaction.user_id}')
                raise AccessDenied()

            self.state.is_update = True
            self.state.prev_amount = self._transaction.amount
            self.state.prev_account_id = self._transaction.account_id
            self.state.prev_new_balance = self._transaction.new_balance
            self.state.prev_account = self._transaction.account
            self.state.prev_target_account_id = self._transaction.target_account_id
            self.state.prev_target_new_balance = self._transaction.target_new_balance
            self.state.prev_target_amount = self._transaction.target_amount
            self.state.prev_is_transfer = self._transaction.is_transfer
            self.state.prev_is_income = self._transaction.is_income
        else:
            self.state.is_update = False
            self.state.prev_amount = Decimal(0.0)
            self.state.prev_target_amount = Decimal(0.0)

            self._transaction = Transaction()
            self._transaction.user_id = self.state.user_id

        return self

    def get_transaction(self) -> Transaction:
        return self._transaction

    def process(self) -> 'TransactionManager':
        if self._transaction.is_transfer:
            self._process_transfer_type()
        else:
            self._process_non_transfer_type()
        self.state.db.add(self._transaction)
        self.state.db.add(self._transaction.account)
        self.state.db.commit()
        self.state.db.refresh(self._transaction)
        self.state.db.refresh(self._transaction.account)

        return self

    def delete_transaction(self) -> 'TransactionManager':
        if self._transaction.is_transfer:
            self.update_acc_prev_transfer()
        else:
            self.update_acc_prev_nontransfer()

        self._transaction.is_deleted = True
        self.state.db.add(self._transaction)
        self.state.db.commit()

        return self

    def _process_transfer_type(self) -> None:
        if self._transaction.account.currency_id != self._transaction.target_account.currency_id:
            currency_processor = CurrencyProcessor(self._transaction, self.state.db)
            self._transaction = currency_processor.calculate_exchange_rate()

        if self.state.is_update:
            self.update_acc_prev_transfer()

        self._transaction.account.balance -= self._transaction.amount
        self._transaction.target_account.balance += self._transaction.target_amount
        self._transaction.new_balance = self._transaction.account.balance
        self._transaction.target_new_balance = self._transaction.target_account.balance

    def update_acc_prev_transfer(self):
        if self.state.prev_is_transfer:
            prev_target_account = self.state.db.query(Account).filter_by(
                id=self.state.prev_target_account_id).one()
            prev_target_account.balance -= self.state.prev_target_amount

            prev_account = self.state.db.query(Account).filter_by(id=self.state.prev_account_id).one()
            prev_account.balance += self.state.prev_amount
            self.state.db.add(prev_target_account)
            self.state.db.add(prev_account)
            self.state.db.commit()
        else:
            if self.state.prev_is_income:
                self._transaction.account.balance -= self.state.prev_amount
            else:
                self._transaction.account.balance += self.state.prev_amount

    def _process_non_transfer_type(self):
        try:
            category = self.state.db.query(UserCategory).filter_by(id=self._transaction.category_id).one()
        except NoResultFound:
            logger.error(f'Invalid category {self._transaction.category_id}')
            raise InvalidCategory()

        if category.user_id != self.state.user_id:
            logger.error(f'User {self.state.user_id} tried to update transaction {self._transaction.id} ' +
                         f'with not own category {self._transaction.category_id}')
            raise AccessDenied()

        self.update_acc_prev_nontransfer()

        if self._transaction.is_income:
            self._transaction.account.balance += self._transaction.amount
        else:
            self._transaction.account.balance -= self._transaction.amount
        self._transaction.new_balance = self._transaction.account.balance

    def update_acc_prev_nontransfer(self):
        if self.state.is_update:
            if self.state.prev_is_income:
                self.state.prev_account.balance -= self.state.prev_amount  # type: ignore
            else:
                self.state.prev_account.balance += self.state.prev_amount  # type: ignore
            self.state.db.add(self.state.prev_account)
