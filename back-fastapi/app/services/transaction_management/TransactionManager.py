from datetime import datetime, timezone
from decimal import Decimal

from icecream import ic
from pydantic import BaseModel, ConfigDict
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.logger_config import logger
from app.models.Account import Account
from app.models.Currency import Currency
from app.models.Transaction import Transaction
from app.schemas.transaction_schema import UpdateTransactionSchema, CreateTransactionSchema
from app.services.errors import AccessDenied, InvalidAccount, InvalidCurrency
from app.services.transaction_management.NonTransferTypeTransaction import NonTransferTypeTransaction
from app.services.transaction_management.TransferTypeTransaction import TransferTypeTransaction
from app.services.transaction_management.errors import InvalidTransaction

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
    def __init__(self, transaction_details: UpdateTransactionSchema | CreateTransactionSchema, user_id: int,
                 db: Session):
        self.state = TransactionState(user_id=user_id, db=db, transaction_details=transaction_details)
        self._transaction: Transaction = Transaction()  # main entity for current transaction
        self._prepare_transaction().set_account(transaction_details.account_id).set_currency().set_date_time(
            transaction_details.date_time)

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

    def _prepare_transaction(self) -> 'TransactionManager':
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

        if self._transaction.is_transfer:
            update_transactions_new_balances(self._transaction.account_id, self.state.db)
            update_transactions_new_balances(self._transaction.target_account_id, self.state.db)
        else:
            update_transactions_new_balances(self._transaction.account_id, self.state.db)


        return self

    def delete_transaction(self) -> 'TransactionManager':
        if self._transaction.is_transfer:
            transfer_type_transaction = TransferTypeTransaction(self._transaction, self.state, self.state.db)
            transfer_type_transaction.update_acc_prev_transfer()
        else:
            non_transfer_transaction = NonTransferTypeTransaction(self._transaction, self.state, self.state.db)
            non_transfer_transaction.update_acc_prev_nontransfer()

        self._transaction.is_deleted = True
        self.state.db.add(self._transaction)
        self.state.db.commit()

        return self

    def _process_transfer_type(self) -> None:
        transfer_type_transaction = TransferTypeTransaction(self._transaction, self.state, self.state.db)
        transfer_type_transaction.process()

    def _process_non_transfer_type(self):
        non_transfer_transaction = NonTransferTypeTransaction(self._transaction, self.state, self.state.db)
        non_transfer_transaction.process()


def update_transactions_new_balances(account_id: int, db: Session) -> bool:
    """ Update all transactions new_balance field for given account_id """
    transactions = (db.query(Transaction)
                    .filter(Transaction.is_deleted == False)
                    .filter(or_(Transaction.account_id == account_id,
                                Transaction.target_account_id == account_id))
                    .order_by(Transaction.date_time.asc())).all()

    for idx, transaction in enumerate(transactions):
        if not transaction.is_transfer:  # update non-transfer type transaction balance
            if transaction.is_income:
                if idx == 0:
                    transaction.new_balance = transaction.account.initial_balance + transaction.amount
                else:
                    transaction.new_balance = transactions[idx - 1].new_balance + transaction.amount
            else:
                if idx == 0:
                    transaction.new_balance = transaction.account.initial_balance - transaction.amount
                else:
                    transaction.new_balance = transactions[idx - 1].new_balance - transaction.amount
        else:  # update transfer type transaction balance
            if transaction.account_id == account_id:
                if idx == 0:
                    transaction.new_balance = transaction.account.initial_balance - transaction.amount
                else:
                    transaction.new_balance = transactions[idx - 1].new_balance - transaction.amount
            #  no need to update target account balance as it should be updated
            #  in call for this function with target_account_id

        db.add(transaction)
    db.commit()

    return True
