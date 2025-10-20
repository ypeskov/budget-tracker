from datetime import date, timedelta

from icecream import ic
from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

from app.logger_config import logger
from app.models.Account import Account
from app.models.Currency import Currency
from app.models.Transaction import Transaction
from app.models.User import User
from app.models.UserCategory import UserCategory
from app.services.CurrencyProcessor import calc_amount

ic.configureOutput(includeContext=True)


class ExpensesReportGenerator:
    def __init__(
        self,
        user_id,
        db: Session,
        start_date: date,
        end_date: date,
        hide_empty_categories: bool = False,
    ):
        self._db = db
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        self.hide_empty_categories = hide_empty_categories

        self._user_categories_with_expenses: list = []

    def prepare_data(self):
        user_categories = self._get_flat_user_categories()

        categories_ids = user_categories.keys()

        query = (
            select(
                UserCategory.name.label('category_name'),
                UserCategory.id.label('category_id'),
                UserCategory.parent_id.label('parent_category_id'),
                Transaction.amount.label('amount'),
                Currency.code.label('currency'),
            )
            .join(UserCategory, Transaction.category_id == UserCategory.id)
            .join(Account, Transaction.account_id == Account.id)
            .join(Currency, Account.currency_id == Currency.id)
            .where(
                Transaction.date_time >= self.start_date,
                Transaction.date_time < (self.end_date + timedelta(days=1)),
                Transaction.is_income == False,
                Transaction.is_deleted == False,
                Transaction.is_transfer == False,
                Transaction.category_id.in_(categories_ids),
            )
            .order_by(UserCategory.name, UserCategory.parent_id)
        )

        result = self._db.execute(query).all()

        user: User = self._db.get(User, self.user_id)  # type: ignore
        base_currency: Currency = user.base_currency

        for row in result:
            # Calculate amount in base currency
            transaction_amount = calc_amount(row.amount, row.currency, self.start_date, base_currency.code, self._db)
            user_categories[row.category_id]['total_expenses'] += transaction_amount
            user_categories[row.category_id]['currency_code'] = base_currency.code

        self._user_categories_with_expenses = list(user_categories.values())

        if self.hide_empty_categories:
            self._user_categories_with_expenses = [
                category for category in self._user_categories_with_expenses if category['total_expenses'] > 0
            ]

        return self

    def get_expenses(self):
        return self._user_categories_with_expenses

    def _get_flat_user_categories(self):
        """Get all user categories in a flat structure ordered by name and children go right after their parent"""
        parent_alias = aliased(UserCategory)

        query = (
            select(
                UserCategory.id.label('category_id'),
                UserCategory.name.label('category_name'),
                UserCategory.parent_id.label('parent_category_id'),
                parent_alias.name.label('parent_category_name'),
            )
            .join(parent_alias, UserCategory.parent_id == parent_alias.id, isouter=True)
            .where(
                UserCategory.user_id == self.user_id,
                UserCategory.is_deleted == False,
                UserCategory.is_income == False,
            )
            .order_by(UserCategory.name)
        )

        categories = self._db.execute(query).all()

        structured_categories = {}

        for category in categories:
            if category.parent_category_id is None:
                structured_categories[category.category_id] = {
                    'id': category.category_id,
                    'name': category.category_name,
                    'children': [],
                }

        for category in categories:
            if category.parent_category_id is not None:
                structured_categories[category.parent_category_id]['children'].append(
                    {
                        'id': category.category_id,
                        'name': category.category_name,
                        'parent_id': category.parent_category_id,
                        'parent_name': category.parent_category_name,
                    }
                )

        flat_categories = {}

        for category in structured_categories.values():  # type: ignore
            flat_categories[int(category['id'])] = {  # type: ignore
                'id': int(category['id']),  # type: ignore
                'name': category['name'],  # type: ignore
                'parent_id': None,
                'parent_name': None,
                'total_expenses': 0,
                'isParent': True,
            }

            for child in category['children']:  # type: ignore
                flat_categories[int(child['id'])] = {
                    'id': int(child['id']),
                    'name': f"{category['name']} >> {child['name']}",  # type: ignore
                    'parent_id': child['parent_id'],
                    'parent_name': child['parent_name'],
                    'total_expenses': 0,
                    'is_parent': False,
                }

        return flat_categories
