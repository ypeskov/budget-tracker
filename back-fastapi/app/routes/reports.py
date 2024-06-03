from fastapi import APIRouter, Depends, HTTPException, status, Request
from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.reports_schema import CashFlowReportInputSchema, CashFlowReportOutputSchema, BalanceReportInputSchema, \
    BalanceReportOutputSchema
from app.services.errors import AccessDenied
from app.services.reports import get_cash_flows, get_balance_report

ic.configureOutput(includeContext=True)

router = APIRouter(
    tags=['Reports'],
    prefix='/reports',
    dependencies=[Depends(check_token)],
)


@router.post('/cashflow/', response_model=CashFlowReportOutputSchema)
def cash_flow(request: Request,
              input_data: CashFlowReportInputSchema,
              db: Session = Depends(get_db)) -> list[dict]:
    """ Get all expenses for one account within a given time period """
    logger.info(f"Getting cash flow report for user_id: {request.state.user['id']}, "
                f"start_date: {input_data.start_date}, "
                f"end_date: {input_data.end_date}, period: {input_data.period}")
    try:
        result: list[dict] = get_cash_flows(request.state.user['id'],
                                            db,
                                            input_data.start_date,
                                            input_data.end_date,
                                            input_data.period)
        return result
    except AccessDenied as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error generting report')


@router.post('/balance/', response_model=list[BalanceReportOutputSchema])
# @router.post('/balance/')
def balance_report(request: Request,
                   input_data: BalanceReportInputSchema,
                   db: Session = Depends(get_db)) -> list[dict]:
    """ Get all expenses for one account within a given time period """
    logger.info(f"Getting balance report for user_id: {request.state.user['id']}, "
                f"account_ids: {input_data.account_ids}, date: {input_data.balance_date}")
    try:
        result: list[dict] = get_balance_report(request.state.user['id'],
                                                db,
                                                input_data.account_ids,
                                                input_data.balance_date)
        return result
    except AccessDenied as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error generting report')
