from app.models.Account import Account
from app.services.CurrencyProcessor import CurrencyProcessor


class TransferTypeTransaction:
    def __init__(self, transaction, state, db):
        self._transaction = transaction
        self.state = state
        self._db = db

    def process(self) -> 'TransferTypeTransaction':
        if self._transaction.account.currency_id != self._transaction.target_account.currency_id:
            currency_processor = CurrencyProcessor(self._transaction, self.state.db)
            self._transaction = currency_processor.calculate_exchange_rate()

        if self.state.is_update:
            self.update_acc_prev_transfer()

        self._transaction.account.balance -= self._transaction.amount
        self._transaction.target_account.balance += self._transaction.target_amount
        self._transaction.target_new_balance = self._transaction.target_account.balance

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
