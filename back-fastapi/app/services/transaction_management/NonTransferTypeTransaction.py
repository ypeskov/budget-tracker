from sqlalchemy.exc import NoResultFound

from app.logger_config import logger
from app.models.UserCategory import UserCategory
from app.services.errors import InvalidCategory, AccessDenied


class NonTransferTypeTransaction:
    def __init__(self, transaction, state, db):
        self._transaction = transaction
        self.state = state
        self._db = db

    def process(self) -> 'NonTransferTypeTransaction':
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

        return self

    def update_acc_prev_nontransfer(self):
        if self.state.is_update:
            if self.state.prev_is_income:
                self.state.prev_account.balance -= self.state.prev_amount  # type: ignore
            else:
                self.state.prev_account.balance += self.state.prev_amount  # type: ignore
            self.state.db.add(self.state.prev_account)
