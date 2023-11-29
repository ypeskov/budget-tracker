from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.logger_config import logger
from app.database import get_db

from app.models.Currency import Currency
from app.models.Transaction import Transaction
from app.models.Account import Account

from app.schemas.transaction_schema import CreateTransactionSchema


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
    def __init__(self, transaction_details: CreateTransactionSchema, user_id: int, db: Session):
        self._db = db
        self._transaction_details = transaction_details
        self._transaction_details.user_id = user_id

        self._transaction: Transaction = Transaction()
        self._transaction.user_id = user_id

        self.set_account(transaction_details.account_id)
        self.set_currency()

        self._transaction.amount = transaction_details.amount
        self._transaction.label = transaction_details.label
        self._transaction.notes = transaction_details.notes

        self.set_date_time(transaction_details.date_time)

        if transaction_details.is_transfer is True:
            self.set_account(transaction_details.target_account_id, 'target_')
            self._transaction.is_transfer = True
            self._transaction.exchange_rate = transaction_details.exchange_rate
            self._transaction.target_amount = transaction_details.target_amount
        else:
            self._transaction.is_transfer = False
            self._transaction.category_id = transaction_details.category_id
            self._transaction.is_income = transaction_details.is_income

    def set_date_time(self, date_time: str = None) -> 'TransactionManager':
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

    def set_account(self, account_id: int = None, account_prefix: str = '') -> 'TransactionManager':
        try:
            check_account_ownership(self._transaction.user_id, account_id, self._db)
            setattr(self._transaction, f'{account_prefix}account_id', account_id)
            account: Account = self._db.query(Account).filter_by(id=account_id).one_or_none()  # type: ignore
            setattr(self._transaction, f'{account_prefix}account', account)
        except HTTPException as e:
            logger.error(f'Error checking account ownership: {e.detail}')
            raise e
        return self

    def get_transaction(self) -> Transaction:
        return self._transaction
