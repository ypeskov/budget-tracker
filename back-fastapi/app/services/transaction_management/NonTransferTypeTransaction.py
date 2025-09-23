from typing import cast

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.logger_config import logger
from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.UserCategory import UserCategory
from app.services.errors import AccessDenied, InvalidCategory


class NonTransferTypeTransaction:
    def __init__(self, transaction, prev_transaction_state: Transaction, db: Session, is_update=False):
        self._transaction = transaction
        self._prev_transaction_state = prev_transaction_state
        self._db = db
        self._is_update = is_update

    def process(self) -> 'NonTransferTypeTransaction':
        if not self._transaction.is_transfer:
            try:
                category: UserCategory = cast(UserCategory,
                                              self._db.query(UserCategory).filter_by(id=self._transaction.category_id).one())
                if not is_category_valid(category, self._transaction.is_income):
                    raise InvalidCategory()
            except NoResultFound:
                logger.error(f'Invalid category {self._transaction.category_id}')
                raise InvalidCategory()

            if category.user_id != self._transaction.user_id:
                logger.error(f'User {self._transaction.user_id} tried to update transaction {self._transaction.id} ' +
                             f'with not own category {self._transaction.category_id}')
                raise AccessDenied()

        #  remove previous transaction amount from account balance
        if self._is_update:
            self.correct_prev_balance()

        if self._transaction.is_income:
            self._transaction.account.balance += self._transaction.amount
        else:
            self._transaction.account.balance -= self._transaction.amount

        return self

    def correct_prev_balance(self):
        # Check if the account has changed
        if self._prev_transaction_state.account_id != self._transaction.account_id:
            # Account changed - need to fetch the previous account from DB to update its balance
            prev_account = self._db.query(Account).filter_by(id=self._prev_transaction_state.account_id).one()

            if self._prev_transaction_state.is_income:
                prev_account.balance -= self._prev_transaction_state.amount
            else:
                prev_account.balance += self._prev_transaction_state.amount

            self._db.add(prev_account)
        else:
            # Same account - adjust current account's balance
            if self._prev_transaction_state.is_income:
                self._transaction.account.balance -= self._prev_transaction_state.amount
            else:
                self._transaction.account.balance += self._prev_transaction_state.amount


def is_category_valid(category: UserCategory, is_income: bool) -> bool:
    income_type = 'income' if is_income else 'expense'
    if category.is_income != is_income:
        logger.error(f'User category [{category.id}] is not [{income_type}] category as requested in transaction')
        raise InvalidCategory()

    return True



