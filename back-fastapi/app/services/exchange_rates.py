from icecream import ic
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.logger_config import logger
from app.models.ExchangeRateHistory import ExchangeRateHistory

ic.configureOutput(includeContext=True)


def get_exchange_rates(db: Session):
    """ Get all exchange rates """
    try:
        exchange_rates = db.query(ExchangeRateHistory).all()
        return exchange_rates
    except Exception as e:  # pragma: no cover
        logger.exception(e)
        raise
