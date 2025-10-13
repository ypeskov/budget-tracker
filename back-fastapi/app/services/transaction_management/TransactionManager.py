import copy
from datetime import datetime, timezone

from icecream import ic
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import select

from app.logger_config import logger
from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.UserCategory import UserCategory
from app.schemas.transaction_schema import (
    CreateTransactionSchema,
    UpdateTransactionSchema,
)
from app.services.errors import AccessDenied, InvalidAccount, InvalidCategory
from app.services.transaction_management.errors import InvalidTransaction
from app.services.transaction_management.NonTransferTypeTransaction import (
    NonTransferTypeTransaction,
)
from app.services.transaction_management.TransferTypeTransaction import (
    TransferTypeTransaction,
)
from app.tasks.tasks import run_user_budgets_update

ic.configureOutput(includeContext=True)


class TransactionManager:
    def __init__(
        self,
        transaction_details: UpdateTransactionSchema | CreateTransactionSchema,
        user_id: int,
        db: Session,
    ):
        self.user_id = user_id
        self.db = db
        self.transaction_details = transaction_details
        self._transaction: Transaction = Transaction()  # main entity for current transaction
        self.prev_transaction_state = Transaction()  # remember state of transaction before update
        self.is_update = True if transaction_details.id is not None else False

        self._prepare_transaction()
        self._set_account(self.transaction_details.account_id)
        self._set_date_time(self.transaction_details.date_time)
        if not transaction_details.is_transfer:
            self._set_category(self.transaction_details.category_id)

    def _set_date_time(self, date_time: datetime | None = None) -> 'TransactionManager':
        self._transaction.date_time = date_time or datetime.now(timezone.utc)
        return self

    def _set_account(self, account_id: int) -> 'TransactionManager':
        try:
            account: Account = self.db.execute(select(Account).where(Account.id == account_id)).scalar_one()
        except NoResultFound:
            logger.error(f'Account {account_id} not found')
            raise InvalidAccount()

        if account.user_id != self.user_id:
            logger.error(f'User {self.user_id} tried to create transaction with not own account {account_id}')
            raise AccessDenied()
        self._transaction.account_id = account.id
        self._transaction.account = account

        return self

    def _set_category(self, category_id) -> 'TransactionManager':
        category: UserCategory = self.db.execute(select(UserCategory).filter_by(id=category_id)).scalar_one_or_none()
        if category is None:
            logger.error(f'Category {category_id} not found')
            raise InvalidCategory()
        if category.user_id != self.user_id:
            logger.error(f'User {self.user_id} tried to create transaction with not own category {category_id}')
            raise AccessDenied()
        self._transaction.category_id = category.id
        self._transaction.category = category

        return self

    def _prepare_transaction(self) -> 'TransactionManager':
        if self.transaction_details.id is not None:
            self._transaction = (
                self.db.query(Transaction)  # type: ignore
                .options(joinedload(Transaction.account), joinedload(Transaction.category))
                .filter_by(id=self.transaction_details.id)
                .one_or_none()
            )
            self.prev_transaction_state = copy.deepcopy(self._transaction)

            if self._transaction is None:
                logger.error(f'Transaction {self.transaction_details.id} not found')
                raise InvalidTransaction(detail=f'Transaction {self.transaction_details.id} not found')

            if self.user_id != self._transaction.user_id:
                logger.error(
                    f'User {self.user_id} tried to update transaction [{self._transaction.id}] of user '
                    + f'{self._transaction.user_id}'
                )
                raise AccessDenied()

            # self.is_update = True
        else:
            self._transaction.user_id = self.user_id

        self._transaction.amount = self.transaction_details.amount
        self._transaction.label = self.transaction_details.label
        self._transaction.notes = str(self.transaction_details.notes)
        self._transaction.is_income = self.transaction_details.is_income
        self._transaction.is_transfer = self.transaction_details.is_transfer

        return self

    def get_transaction(self) -> Transaction:
        return self._transaction

    def process(self) -> 'TransactionManager':
        if self._transaction.is_transfer:
            self._process_transfer_type()
        else:
            self._process_non_transfer_type()
            self.db.add(self._transaction)

        self.db.commit()

        #  update budgets if transaction is not transfer
        if not self._transaction.is_transfer and not self._transaction.is_income:
            run_user_budgets_update.delay(self.user_id)

        update_transactions_new_balances(self._transaction.account_id, self.db)
        if self._transaction.is_transfer:
            update_transactions_new_balances(self.transaction_details.target_account_id, self.db)  # type: ignore

        return self

    def delete_transaction(self) -> 'TransactionManager':
        direct_transaction_type = NonTransferTypeTransaction(self._transaction, self.prev_transaction_state, self.db)
        direct_transaction_type.correct_prev_balance()

        #  if transaction is transfer, we need to delete linked transaction too
        if self._transaction.is_transfer:
            indirect_transaction_id: int = self._transaction.linked_transaction_id
            indirect_transaction: Transaction = self.db.execute(
                select(Transaction).filter_by(id=indirect_transaction_id)
            ).scalar_one()
            prev_indirect_transaction_state: Transaction = copy.deepcopy(indirect_transaction)
            indirect_transaction.is_deleted = True
            indirect_transaction_type = NonTransferTypeTransaction(
                indirect_transaction, prev_indirect_transaction_state, self.db
            )
            indirect_transaction_type.correct_prev_balance()
            self.db.add(indirect_transaction)
        else:
            run_user_budgets_update.delay(self.user_id)

        self._transaction.is_deleted = True
        self.db.add(self._transaction)
        self.db.commit()

        return self

    def _process_transfer_type(self) -> None:
        transfer_type_transaction = TransferTypeTransaction(
            self._transaction,
            self.prev_transaction_state,
            self.db,
            is_update=self.is_update,
        )
        transfer_type_transaction.process(self.transaction_details)

    def _process_non_transfer_type(self) -> 'TransactionManager':
        non_transfer_transaction = NonTransferTypeTransaction(
            self._transaction,
            self.prev_transaction_state,
            self.db,
            is_update=self.is_update,
        )
        non_transfer_transaction.process()
        return self


def update_transactions_new_balances(account_id: int, db: Session) -> bool:
    """Update all transactions new_balance field for given account_id"""
    transactions = (
        db.query(Transaction)
        .filter(Transaction.is_deleted == False)  # noqa: E712
        .filter(Transaction.account_id == account_id)
        .order_by(Transaction.date_time.asc())
        .all()
    )
    for idx, transaction in enumerate(transactions):
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

        db.add(transaction)
    db.commit()

    return True
