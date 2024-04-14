from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from icecream import ic

from app.logger_config import logger
from app.database import get_db
from app.dependencies.check_token import check_token
from app.models.ExchangeRateHistory import ExchangeRateHistory

ic.configureOutput(includeContext=True)

router = APIRouter(
    tags=['ExchangeRates'],
    prefix='/exchange-rates',
    dependencies=[Depends(check_token)]
)


@router.get('/')
def get_exchange_rates(request: Request, db: Session = Depends(get_db)):
    """ Get all exchange rates """
    try:
        exchange_rates = db.query(ExchangeRateHistory).all()
        return exchange_rates
    except Exception as e:  # pragma: no cover
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to get exchange rates')


@router.get('/update')
def update_exchange_rates(request: Request, db: Session = Depends(get_db)):
    """ Update exchange rates """
    try:
        pass
    except Exception as e:  # pragma: no cover
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to update exchange rates')
