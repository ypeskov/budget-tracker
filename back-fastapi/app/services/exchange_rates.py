from datetime import date

from icecream import ic
from sqlalchemy.orm import Session

from app.logger_config import logger
from app.models.ExchangeRateHistory import ExchangeRateHistory
from app.services.exchange_services.CurrencyBeacon import CurrencyBeaconService
from app.services.exchange_services.AbstractCurrencyService import AbstractCurrencyService

ic.configureOutput(includeContext=True)


def get_exchange_rates(db: Session, when: date | str = '') -> ExchangeRateHistory:
    """ Get all exchange rates for defined date"""
    try:
        stmt = db.query(ExchangeRateHistory)
        filters = []
        if when == '':
            filters.append(ExchangeRateHistory.actual_date == date.today())
        elif when == 'latest':
            stmt = stmt.order_by(ExchangeRateHistory.actual_date.desc())
        else:
            filters.append(ExchangeRateHistory.actual_date == when)
        exchange_rates: ExchangeRateHistory = stmt.filter(*filters).one()  # noqa

        return exchange_rates
    except Exception as e:  # pragma: no cover
        logger.exception(e)
        raise


def update_exchange_rates(db: Session, when: date) -> ExchangeRateHistory:
    """ Add/Update exchange rates for defined date"""
    try:
        currency_service: AbstractCurrencyService = CurrencyBeaconService()
        prev_exchange_rates: ExchangeRateHistory = db.query(ExchangeRateHistory).filter(  # type: ignore
            ExchangeRateHistory.actual_date == when).one_or_none()
        if prev_exchange_rates:
            db.delete(prev_exchange_rates)
            db.flush()
        exchange_rates = ExchangeRateHistory(**currency_service.get_currency_rates(when.isoformat()))
        db.add(exchange_rates)
        db.commit()
        return exchange_rates
    except Exception as e:  # pragma: no cover
        logger.exception(e)
        raise
