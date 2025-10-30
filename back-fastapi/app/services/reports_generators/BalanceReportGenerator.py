from datetime import date, datetime, timedelta
from decimal import Decimal

from icecream import ic
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.Account import Account
from app.models.Currency import Currency
from app.models.User import User
from app.services.CurrencyProcessor import calc_amount

ic.configureOutput(includeContext=True)


class BalanceReportGenerator:
    def __init__(
        self,
        user_id: int,
        account_ids: list,
        db: Session,
        balance_date: date | None = None,
    ):
        self.account_ids = account_ids
        self.user_id = user_id
        self.db = db

        if balance_date is None:
            balance_date = datetime.now().date()
        self.balance_date = balance_date

        self.raw_results = None

        self.user_base_currency = (
            db.query(Currency).join(User, User.base_currency_id == Currency.id).filter(User.id == user_id).one()
        )

    def prepare_raw_data(self) -> 'BalanceReportGenerator':
        filters = [
            Account.user_id == self.user_id,
        ]

        if self.account_ids:
            filters.append(Account.id.in_(self.account_ids))
        else:
            filters.append(Account.show_in_reports == True)

        self.raw_results = (
            self.db.query(  # type: ignore
                Account.id,
                Account.balance,
                Account.name,
                Account.show_in_reports,
                Currency.code,
            )
            .join(Currency, Account.currency_id == Currency.id)
            .filter(and_(*filters))
            .order_by(Account.name)
            .all()
        )

        return self

    def get_balances(self) -> list[dict]:
        balance_data = []
        balance_date = self.balance_date
        for result in self.raw_results:  # type: ignore
            balance = result.balance if result else 0
            account_name = result.name if result else ''
            currency_code = result.code if result else ''

            # calculate in the same currency
            if balance != 0:
                base_currency_balance = calc_amount(
                    balance,
                    currency_code,
                    balance_date,
                    self.user_base_currency.code,
                    self.db,
                )
            else:
                base_currency_balance = Decimal(0)

            balance_data.append(
                {
                    "account_id": result.id,
                    "account_name": account_name,
                    "currency_code": currency_code,
                    "balance": balance,
                    "base_currency_balance": base_currency_balance,
                    "base_currency_code": self.user_base_currency.code,
                    "report_date": balance_date,
                }
            )
        return balance_data
