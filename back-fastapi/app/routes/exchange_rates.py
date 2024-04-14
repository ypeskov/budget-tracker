from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from icecream import ic

from app.logger_config import logger
from app.database import get_db
from app.dependencies.check_token import check_token
from app.services.exchange_services.exceptions import ErrorFetchingData
from app.models.ExchangeRateHistory import ExchangeRateHistory
from app.services.exchange_rates import get_exchange_rates, update_exchange_rates
from app.schemas.exchange_rates_schema import ExchangeRateSchema

ic.configureOutput(includeContext=True)

router = APIRouter(
    tags=['ExchangeRates'],
    prefix='/exchange-rates',
    dependencies=[Depends(check_token)]
)


@router.get('/')
def get_rates(db: Session = Depends(get_db)):
    """ Get all exchange rates """
    try:
        exchange_rates: ExchangeRateHistory = get_exchange_rates(db)
        return exchange_rates
    except Exception as e:  # pragma: no cover
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to get exchange rates')


@router.get('/update/', status_code=status.HTTP_200_OK, response_model=ExchangeRateSchema)
def update_rates(db: Session = Depends(get_db)):
    """ Update exchange rates """
    try:
        exchange_rates: ExchangeRateHistory = update_exchange_rates(db, when=date.today())
        return exchange_rates
    except ErrorFetchingData as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Error while fetching data')
    except Exception as e:  # pragma: no cover
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Unable to update exchange rates')
