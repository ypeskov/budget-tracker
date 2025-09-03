from datetime import date
from typing import Any, Dict, List, cast

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.logger_config import logger
from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.User import User
from app.models.UserCategory import UserCategory
from app.services.CurrencyProcessor import calc_amount


class ExpenseDataProcessor:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    def get_transactions_data(
        self,
        start_date: date,
        end_date: date,
        limit: int = 100 # -1 for all
    ) -> List[Dict[str, Any]]:
        user: User = cast(User, self.db.get(User, self.user_id))
        try:
            query = (
                select(
                    Transaction,
                    UserCategory.name.label('category_name'),
                    Account.name.label('account_name')
                )
                .join(UserCategory, Transaction.category_id == UserCategory.id, isouter=True)
                .join(Account, Transaction.account_id == Account.id)
                .where(
                    Transaction.user_id == self.user_id,
                    Transaction.date_time >= start_date,
                    Transaction.date_time <= end_date,
                    ~Transaction.is_transfer  # Exclude transfers
                )
                .order_by(Transaction.date_time.desc())
            )

            if limit > 0:
                query = query.limit(limit)

            results = self.db.execute(query).all()

            transactions_data = []
            for result in results:
                transaction = result.Transaction
                transactions_data.append({
                    'id': transaction.id,
                    'amount': float(calc_amount(transaction.amount,
                                                transaction.account.currency.code,
                                                transaction.date_time.date(),
                                                user.base_currency.code,
                                                self.db)),
                    'currency': user.base_currency.code,
                    'date': transaction.date_time.strftime('%Y-%m-%d'),
                    'label': transaction.label or '',
                    'category': result.category_name or 'No Category',
                    'account': transaction.account.name or '',
                    'is_income': transaction.is_income
                })

            logger.info(f"Retrieved {len(transactions_data)} transactions for analysis")
            return transactions_data

        except Exception as e:
            logger.error(f"Error retrieving transactions data: {str(e)}")
            return []

    def format_for_analysis(self, transactions: List[Dict[str, Any]]) -> str:
        if not transactions:
            return "No transactions available for analysis."

        # Group by category
        categories = {}
        total_expense = 0
        total_income = 0

        for tx in transactions:
            category = tx['category']
            amount = tx['amount']

            if tx['is_income']:
                total_income += amount
            else:
                total_expense += amount
                if category not in categories:
                    categories[category] = {'amount': 0, 'count': 0, 'transactions': []}
                categories[category]['amount'] += amount
                categories[category]['count'] += 1
                categories[category]['transactions'].append(tx)

        # Format summary
        summary = f"Period: {transactions[-1]['date']} - {transactions[0]['date']}\n"
        summary += f"Total Expenses: {total_expense:.2f}\n"
        summary += f"Total Income: {total_income:.2f}\n\n"

        for tx in transactions:
            summary += f"- {tx['date']}: {tx['amount']:.2f} {tx['currency']} | {tx['label']} | Category: {tx['category']} | Account: {tx['account']}\n"

        return summary

    def get_category_summary(
        self,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        try:
            query = (
                select(
                    UserCategory.name,
                    Transaction.amount.label('amount'),
                    Transaction.is_income
                )
                .join(UserCategory, Transaction.category_id == UserCategory.id, isouter=True)
                .where(
                    Transaction.user_id == self.user_id,
                    Transaction.date_time >= start_date,
                    Transaction.date_time <= end_date,
                    ~Transaction.is_transfer
                )
            )

            results = self.db.execute(query).all()

            category_summary = {}
            for result in results:
                category = result.name or 'No Category'
                amount = float(result.amount)

                if category not in category_summary:
                    category_summary[category] = {'expense': 0, 'income': 0, 'count': 0}

                if result.is_income:
                    category_summary[category]['income'] += amount
                else:
                    category_summary[category]['expense'] += amount

                category_summary[category]['count'] += 1

            return category_summary

        except Exception as e:
            logger.error(f"Error getting category summary: {str(e)}")
            return {}
