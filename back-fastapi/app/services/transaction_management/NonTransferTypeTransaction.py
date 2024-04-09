from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from icecream import ic

from app.logger_config import logger
from app.models.UserCategory import UserCategory
from app.models.Transaction import Transaction
from app.services.errors import InvalidCategory, AccessDenied

ic.configureOutput(includeContext=True)


class NonTransferTypeTransaction:
    def __init__(self, transaction, prev_transaction_state: Transaction, db: Session, is_update=False):
        self._transaction = transaction
        self._prev_transaction_state = prev_transaction_state
        self._db = db
        self._is_update = is_update

    def process(self) -> 'NonTransferTypeTransaction':
        try:
            category = self._db.query(UserCategory).filter_by(id=self._transaction.category_id).one()
            if not is_category_valid(category, self._transaction.is_income):
                raise InvalidCategory()
        except NoResultFound:
            logger.error(f'Invalid category {self._transaction.category_id}')
            raise InvalidCategory()

        if category.user_id != self._transaction.user_id:
            logger.error(f'User {self._transaction.user_id} tried to update transaction {self._transaction.id} ' +
                         f'with not own category {self._transaction.category_id}')
            raise AccessDenied()

        #  self.update_acc_prev_nontransfer()
        ic(self._transaction)
        if self._transaction.is_income:
            self._transaction.account.balance += self._transaction.amount
        else:
            self._transaction.account.balance -= self._transaction.amount
        # self._transaction.new_balance = self._transaction.account.balance

        return self

    def update_acc_prev_nontransfer(self):
        if self._is_update:
            if self.state.prev_is_income:
                self.state.prev_account.balance -= self.state.prev_amount  # type: ignore
            else:
                self.state.prev_account.balance += self.state.prev_amount  # type: ignore
            self.state.db.add(self.state.prev_account)


def is_category_valid(category: UserCategory, is_income: bool) -> bool:
    income_type = 'income' if is_income else 'expense'
    if category.is_income != is_income:
        logger.error(f'User category [{category.id}] is not [{income_type}] category as requested in transaction')
        raise InvalidCategory()

    return True
