from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import TypedDict

from fastapi import HTTPException
from sqlalchemy.orm import Session
from icecream import ic

from app.models.ExchangeRateHistory import ExchangeRateHistory

ic.configureOutput(includeContext=True)

# Global cache to store exchange rates
class CurrencyCache(TypedDict):
    data: dict
    last_updated: datetime | None

currency_cache: CurrencyCache = {"data": {}, "last_updated": None}


def get_exchange_rates_for_year(db: Session):
    """
    Load exchange rates for the last year, apply back-fill and forward-fill for missing dates, and cache them in memory.
    """
    global currency_cache
    today = date.today()
    one_year_ago = today - timedelta(days=365)

    if not is_cache_valid():
        rows = fetch_exchange_rate_rows(db, one_year_ago)
        rates = fill_exchange_rates(rows, one_year_ago, today)
        update_cache(rates)

    return currency_cache["data"]


def is_cache_valid():
    """
    Check if the cache is still valid (updated within the last 24 hours).
    """
    if not currency_cache["last_updated"]:
        return False
    return (datetime.now() - currency_cache["last_updated"]).total_seconds() <= 86400  # 24 hours


def fetch_exchange_rate_rows(db: Session, start_date: date):
    """
    Fetch exchange rate rows from the database for dates >= start_date.
    """
    rows = db.query(ExchangeRateHistory).filter(
        ExchangeRateHistory.actual_date >= start_date
    ).order_by(ExchangeRateHistory.actual_date).all()

    if not rows:
        raise ValueError("No exchange rate data available in the database.")
    return rows


def fill_exchange_rates(rows, start_date: date, end_date: date):
    """
    Fill the exchange rates for the given date range using backfill and forward-fill.
    """
    rates = {}
    last_rates = None
    current_date = start_date

    while current_date <= end_date:
        current_date_str = current_date.isoformat()
        last_rates = process_date(rows, current_date, last_rates, rates, current_date_str)
        current_date += timedelta(days=1)

    return rates


def process_date(rows, current_date, last_rates, rates, current_date_str):
    """
    Process a single date, applying back-fill or forward-fill as needed.
    """
    if rows and rows[0].actual_date == current_date:
        # Use the rate for this date
        row = rows.pop(0)
        rates[current_date_str] = row.rates
        return row.rates
    elif last_rates:
        # Use the last available rates for back-fill
        rates[current_date_str] = last_rates
        return last_rates
    else:
        # Forward-fill: Look ahead for the next available rates
        return forward_fill(rows, current_date_str, rates)


def forward_fill(rows, current_date_str, rates):
    """
    Apply forward-fill logic to find the next available rates.
    """
    if rows:
        # Use the next available rates in the future
        next_row = rows.pop(0)
        rates[current_date_str] = next_row.rates
        return next_row.rates
    else:
        # If no rates exist in the future, raise an error
        raise ValueError(f"No exchange rate data available for {current_date_str} or any earlier/later dates.")


def update_cache(rates):
    """
    Update the global cache with the newly generated rates.
    """
    currency_cache["data"] = rates
    currency_cache["last_updated"] = datetime.now()


def calc_amount(src_amount: Decimal,
                currency_code_from: str,
                calc_date: date,
                user_base_currency_code: str,
                db: Session) -> Decimal:
    """
    Calculate the amount in the user's base currency using exchange rates.

    Parameters:
    - src_amount: Decimal, the amount in the source currency.
    - currency_code_from: str, the source currency code.
    - calc_date: date, the date of the transaction.
    - user_base_currency_code: str, the user's base currency code.
    - db: Session, the database session to query exchange rates.

    Returns:
    - Decimal: The converted amount in the user's base currency.
    """
    if currency_code_from == user_base_currency_code:
        return src_amount

        # Load exchange rates for the last year (from cache or database)
    exchange_rates = get_exchange_rates_for_year(db)

    calc_date_str = calc_date.isoformat()

    # Check if rates for the calculation date exist
    if calc_date_str not in exchange_rates:
        raise HTTPException(500, f'Exchange rates not found for {calc_date_str}')

    # Retrieve the rates for the given date
    rates = exchange_rates[calc_date_str]

    # Get the exchange rate for the source currency
    exchange_rate_HBCR = rates.get(currency_code_from)
    if exchange_rate_HBCR is None:
        raise HTTPException(500, f'Exchange rate not found for {currency_code_from}')

    # Get the exchange rate for the user's base currency
    user_base_currency_rate = rates.get(user_base_currency_code)
    if user_base_currency_rate is None:
        raise HTTPException(500, f'Exchange rate not found for {user_base_currency_code}')

    # Perform the conversion
    converted_amount = src_amount / Decimal(exchange_rate_HBCR) * Decimal(user_base_currency_rate)

    return converted_amount
