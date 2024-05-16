from datetime import date
from decimal import Decimal

from fastapi import HTTPException
from icecream import ic
from sqlalchemy.orm import Session

from app.models.ExchangeRateHistory import ExchangeRateHistory
from app.models.Transaction import Transaction

ic.configureOutput(includeContext=True)


class CurrencyProcessor:
    def __init__(self, transaction: Transaction, db: Session):
        self.transaction = transaction
        self.db = db

    def calculate_exchange_rate(self):
        if self.transaction is None:
            raise HTTPException(422, 'Transaction is required')

        exchange_rate: Decimal | None = self.transaction.exchange_rate
        target_amount: Decimal | None = self.transaction.target_amount
        if exchange_rate is None and target_amount is None:
            raise HTTPException(422, 'Exchange rate or target amount are required')

        if target_amount is None:
            target_amount = self.transaction.amount * exchange_rate  # type: ignore
            self.transaction.target_amount = target_amount
        elif exchange_rate is None:
            exchange_rate = target_amount / self.transaction.amount
            self.transaction.exchange_rate = exchange_rate
        return self.transaction


def calc_amount(src_amount: Decimal,
                currency_code_from: str,
                calc_date: date,
                user_base_currency_code: str,
                db: Session) -> Decimal:
    """ Calculate amount in user base currency. Exchange  rate is taken from history where base currency is USD.
     src_amount: amount in source currency
     currency_code_from: source currency code
     calc_date: date of calculation
     user_base_currency_code: user base currency code
     db: database session
     """
    subquery = db.query(ExchangeRateHistory).filter(
        ExchangeRateHistory.actual_date <= calc_date
    ).order_by(
        ExchangeRateHistory.actual_date.desc()
    ).limit(1).subquery()

    exchange_rates = db.query(subquery.c.rates).one()
    ic(exchange_rates.rates)

    if currency_code_from == user_base_currency_code:
        return src_amount
    else:
        # Get exchange rate from base currency in history to source currency
        exchange_rate_HBCR = exchange_rates.rates.get(currency_code_from, None)
        if exchange_rate_HBCR is None:
            raise HTTPException(500, f'Exchange rate not found for {currency_code_from}')

        user_base_currency_rate = exchange_rates.rates.get(user_base_currency_code, None)
        if user_base_currency_rate is None:
            raise HTTPException(500, f'Exchange rate not found for {user_base_currency_code}')

        converted_amount = src_amount / Decimal(exchange_rate_HBCR) * Decimal(user_base_currency_rate)

        return converted_amount
