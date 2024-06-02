from datetime import datetime, date, timedelta

from icecream import ic
from sqlalchemy import func, and_
from sqlalchemy.orm import Session, aliased

from app.models.Account import Account
from app.models.Currency import Currency
from app.models.Transaction import Transaction
from app.models.User import User
from app.services.CurrencyProcessor import calc_amount

ic.configureOutput(includeContext=True)


class BalanceReportGenerator:
    def __init__(self, user_id: int, db: Session, balance_date: date = None):
        self.user_id = user_id
        self.db = db

        if balance_date is None:
            balance_date = datetime.now().date()
        self.balance_date = balance_date

        self.raw_results = None

        self.user_base_currency = db.query(Currency).join(User, User.base_currency_id == Currency.id).filter(
            User.id == user_id).one()

    def prepare_raw_data(self) -> 'BalanceReportGenerator':
        AccountAlias = aliased(Account)

        subquery = (
            self.db.query(
                Transaction.account_id,
                func.max(Transaction.date_time).label('max_date_time')
            )
            .join(AccountAlias, AccountAlias.id == Transaction.account_id)
            .filter(
                and_(
                    Transaction.user_id == self.user_id,
                    Transaction.date_time < self.balance_date + timedelta(days=1),
                    AccountAlias.show_in_reports == True
                )
            )
            .group_by(Transaction.account_id)
            .subquery()
        )

        self.raw_results = (
            self.db.query(
                Transaction.account_id,
                Transaction.new_balance,
                Account.name,
                Account.show_in_reports,
                Currency.code
            )
            .distinct(Transaction.account_id, Account.name, Currency.code)
            .join(subquery,
                  (Transaction.account_id == subquery.c.account_id) &
                  (Transaction.date_time == subquery.c.max_date_time))
            .join(Account, Account.id == Transaction.account_id)
            .join(Currency, Account.currency_id == Currency.id)
            .order_by(Account.name)
            .all()
        )

        return self

    def get_balances(self) -> list[dict]:
        balance_data = []
        balance_date = self.balance_date
        for result in self.raw_results:
            balance = result.new_balance if result else 0
            account_name = result.name if result else ''
            currency_code = result.code if result else ''

            # calculate in the same currency
            if balance != 0:
                base_currency_balance = calc_amount(balance,
                                                    currency_code,
                                                    balance_date,
                                                    self.user_base_currency.code,
                                                    self.db)
            else:
                base_currency_balance = 0

            balance_data.append({"account_id": result.account_id,
                                 "account_name": account_name,
                                 "currency_code": currency_code,
                                 "balance": balance,
                                 "base_currency_balance": base_currency_balance,
                                 "base_currency_code": self.user_base_currency.code,
                                 "report_date": balance_date
                                 })
        return balance_data
