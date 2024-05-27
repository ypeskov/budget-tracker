from datetime import timedelta
from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import case, and_

from app.models.Account import Account
from app.models.Currency import Currency
from app.models.Transaction import Transaction


class CashFlowReportGenerator:
    def __init__(self, user_id, db: Session = None):
        self._db = db
        self.user_id = user_id
        self.account_ids = None
        self.period = None
        self.start_date = None
        self.end_date = None
        self.period_str: str = ''
        self.label: str = ''

        self._accounts_info = None

    def set_parameters(self, account_ids, period='monthly', start_date=None, end_date=None):
        self.account_ids = account_ids
        self.period = period
        self.start_date = start_date
        self.end_date = end_date

    def get_data(self):
        self.prepare_accounts_info()

        return self.get_cash_flows()

    def prepare_accounts_info(self):
        accounts = self._db.query(
            Account.id,
            Account.name,
            Currency.code.label("currency")
        ).filter(
            Account.id.in_(self.account_ids),
            Account.user_id == self.user_id
        ).join(
            Currency, Account.currency_id == Currency.id
        ).all()

        self._accounts_info = {account.id: {"name": account.name, "currency": account.currency} for account in accounts}

    def get_cash_flows(self):
        cash_flows = []
        prepared_results = self.prepare_data()
        for result in prepared_results:
            account_id, period, total_income, total_expenses = result
            total_income = Decimal(total_income or 0)
            total_expenses = Decimal(total_expenses or 0)
            net_flow = total_income - total_expenses

            cash_flow = {
                'account_id': account_id,
                'account_name': self._accounts_info[account_id]["name"],
                'currency': self._accounts_info[account_id]["currency"],
                'total_income': total_income,
                'total_expenses': total_expenses,
                'net_flow': net_flow,
                'period': period,
            }

            cash_flows.append(cash_flow)

        return cash_flows

    def set_label(self):
        if self.period == 'monthly':
            self.label = 'transactions_month'
            self.period_str = 'YYYY-MM'
        elif self.period == 'daily':
            self.label = 'transactions_day'
            self.period_str = 'YYYY-MM-DD'
        else:
            raise ValueError(f"Invalid period: {self.period}")

    def prepare_data(self):
        self.set_label()

        query = (
            self._db.query(
                Account.id.label('account_id'),
                func.to_char(Transaction.date_time, self.period_str).label(self.label),
                func.coalesce(
                    func.sum(
                        case((Transaction.is_income == True, Transaction.amount), else_=0)
                    ).filter(Transaction.is_deleted == False, Transaction.is_transfer == False), 0
                ).label('total_income'),
                func.coalesce(
                    func.sum(
                        case((Transaction.is_income == False, Transaction.amount), else_=0)
                    ).filter(Transaction.is_deleted == False, Transaction.is_transfer == False), 0
                ).label('total_expenses')
            )
            .outerjoin(Transaction,
                       and_(Account.id == Transaction.account_id, Transaction.account_id.in_(self.account_ids)))
            .filter(Account.user_id == self.user_id, Account.id.in_(self.account_ids))
            .group_by(Account.id, func.to_char(Transaction.date_time, self.period_str))
            .order_by(Account.id, self.label)
        )

        additional_filters = []
        if self.start_date:
            additional_filters.append(Transaction.date_time >= self.start_date)
        if self.end_date:
            additional_filters.append(Transaction.date_time <= (self.end_date + timedelta(days=1)))

        if additional_filters:
            query = query.filter(*additional_filters)

        query = query.group_by(Transaction.account_id, Account.id, )
        results = query.all()

        return results
