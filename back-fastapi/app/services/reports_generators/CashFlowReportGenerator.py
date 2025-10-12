from datetime import datetime, timedelta
from decimal import Decimal

from icecream import ic
from sqlalchemy import and_, case
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.Account import Account
from app.models.Currency import Currency
from app.models.Transaction import Transaction
from app.models.User import User
from app.services.CurrencyProcessor import calc_amount

ic.configureOutput(includeContext=True)


class CashFlowReportGenerator:
    def __init__(self, user_id, db: Session):
        self._db = db
        self.user_id = user_id
        self.account_ids: list[int] = []
        self.period = None
        self.start_date = None
        self.end_date = None
        self.period_str: str = ""
        self.label: str = ""

        self._accounts_info: dict = {}

    def set_parameters(self, period="monthly", start_date=None, end_date=None):
        self.period = period
        self.start_date = start_date
        self.end_date = end_date

    def get_data(self):
        self.prepare_accounts_info()

        return self.get_cash_flows()

    def prepare_accounts_info(self):
        accounts = (
            self._db.query(Account.id, Account.name, Currency.code.label("currency"))
            .filter(Account.user_id == self.user_id)
            .join(Currency, Account.currency_id == Currency.id)
            .all()
        )
        self.account_ids = [account.id for account in accounts]

        self._accounts_info = {
            account.id: {"name": account.name, "currency": account.currency}
            for account in accounts
        }

    def get_cash_flows(self):
        prepared_results = self.prepare_data()

        today = datetime.now().date()
        user = self._db.query(User).filter(User.id == self.user_id).one()

        income_sum: dict = {}
        expenses_sum: dict = {}
        net_flow: dict = {}

        for result in prepared_results:
            account_id, period, total_income, total_expenses = result
            income_in_period = Decimal(
                calc_amount(
                    total_income or Decimal(0),
                    self._accounts_info[account_id]["currency"],
                    today,
                    user.base_currency.code,
                    self._db,
                )
            )
            if period not in income_sum:
                income_sum.setdefault(period, income_in_period)
            else:
                income_sum[period] += income_in_period

            expenses_in_period = Decimal(
                calc_amount(
                    total_expenses or Decimal(0),
                    self._accounts_info[account_id]["currency"],
                    today,
                    user.base_currency.code,
                    self._db,
                )
            )
            if period not in expenses_sum:
                expenses_sum.setdefault(period, expenses_in_period)
            else:
                expenses_sum[period] += expenses_in_period

            net_flow_in_period = income_in_period - expenses_in_period
            if period not in net_flow:
                net_flow.setdefault(period, net_flow_in_period)
            else:
                net_flow[period] += net_flow_in_period

        cash_flow = {
            "total_income": income_sum,
            "total_expenses": expenses_sum,
            "net_flow": net_flow,
            "currency": user.base_currency.code,
        }

        return cash_flow

    def set_label(self):
        if self.period == "monthly":
            self.label = "transactions_month"
            self.period_str = "YYYY-MM"
        elif self.period == "daily":
            self.label = "transactions_day"
            self.period_str = "YYYY-MM-DD"
        else:
            raise ValueError(f"Invalid period: {self.period}")

    def prepare_data(self):
        self.set_label()

        query = (
            self._db.query(
                Account.id.label("account_id"),
                func.to_char(Transaction.date_time, self.period_str).label(self.label),
                func.coalesce(
                    func.sum(
                        case(
                            (Transaction.is_income == True, Transaction.amount), else_=0
                        )  # noqa
                    ).filter(
                        Transaction.is_deleted == False,
                        Transaction.is_transfer == False,
                    ),
                    0,
                ).label("total_income"),
                func.coalesce(
                    func.sum(
                        case(
                            (Transaction.is_income == False, Transaction.amount),
                            else_=0,
                        )  # noqa
                    ).filter(
                        Transaction.is_deleted == False,
                        Transaction.is_transfer == False,
                    ),
                    0,
                ).label("total_expenses"),
            )
            .outerjoin(
                Transaction,
                and_(
                    Account.id == Transaction.account_id,
                    Transaction.account_id.in_(self.account_ids),
                ),
            )
            .filter(Account.user_id == self.user_id, Account.id.in_(self.account_ids))
            .group_by(
                Account.id,
                func.to_char(Transaction.date_time, self.period_str),
                Transaction.date_time,
            )
            .order_by(self.label)
        )

        additional_filters = []
        if self.start_date:
            additional_filters.append(Transaction.date_time >= self.start_date)
        else:
            # get start date 12 months ago in case of monthly report and 30 days ago in case of daily report
            if self.period == "monthly":
                additional_filters.append(
                    Transaction.date_time >= (datetime.now() - timedelta(days=365))
                )
            elif self.period == "daily":
                additional_filters.append(
                    Transaction.date_time >= (datetime.now() - timedelta(days=30))
                )

        if self.end_date:
            additional_filters.append(
                Transaction.date_time <= (self.end_date + timedelta(days=1))
            )
        else:
            additional_filters.append(
                Transaction.date_time <= (datetime.now() + timedelta(days=1))
            )

        if additional_filters:
            query = query.filter(*additional_filters)

        results = query.all()

        return results
