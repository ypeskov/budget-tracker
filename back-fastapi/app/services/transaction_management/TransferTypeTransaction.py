import copy

from sqlalchemy.orm import Session

from icecream import ic

from app.models.Account import Account
from app.models.Transaction import Transaction
from app.services.CurrencyProcessor import CurrencyProcessor
from .NonTransferTypeTransaction import NonTransferTypeTransaction
from app.schemas.transaction_schema import UpdateTransactionSchema, CreateTransactionSchema
from ...models.Currency import Currency

ic.configureOutput(includeContext=True)


class TransferTypeTransaction:
    def __init__(self, transaction, prev_transaction_state: Transaction, db: Session, is_update=False):
        self._transaction = transaction
        self._prev_transaction_state = prev_transaction_state
        self._db = db
        self._is_update = is_update

    def process(self,
                transaction_details: UpdateTransactionSchema | CreateTransactionSchema) -> 'TransferTypeTransaction':

        src_account_transaction = NonTransferTypeTransaction(self._transaction,
                                                             self._prev_transaction_state,
                                                             self._db,
                                                             self._is_update)
        src_account_transaction.process()
        target_transaction: Transaction = copy.deepcopy(self._transaction)
        self._db.add(self._transaction)
        self._db.flush()

        if self._is_update:
            target_transaction = self._db.query(Transaction).filter_by(id=self._transaction.linked_transaction_id).one()
            self._prev_transaction_state = copy.deepcopy(target_transaction)
        target_transaction.account_id = transaction_details.target_account_id
        target_transaction.account = self._db.query(Account).filter_by(id=transaction_details.target_account_id).one()
        target_transaction.amount = transaction_details.target_amount
        target_transaction.linked_transaction_id = self._transaction.id
        target_transaction.is_income = not self._transaction.is_income
        target_transaction.currency_id = target_transaction.account.currency_id
        target_transaction.currency = self._db.query(Currency).filter_by(id=target_transaction.currency_id).one()

        target_account_transaction = NonTransferTypeTransaction(target_transaction,
                                                                self._prev_transaction_state,
                                                                self._db,
                                                                self._is_update)
        target_account_transaction.process()

        self._db.add(target_transaction)
        self._db.flush()
        self._transaction.linked_transaction_id = target_transaction.id

        return self

    def update_acc_prev_transfer(self):
        if self.state.prev_is_transfer:
            prev_target_account = self.state.db.query(Account).filter_by(id=self.state.prev_target_account_id).one()
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
