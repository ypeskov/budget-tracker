from fastapi import APIRouter, Depends, HTTPException, status, Request
from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.reports_schema import (CashFlowReportInputSchema, CashFlowReportOutputSchema,
                                        BalanceReportInputSchema, BalanceReportOutputSchema,
                                        ExpensesReportInputSchema, ExpensesReportOutputItemSchema)
from app.services.errors import AccessDenied
from app.services.reports import get_cash_flows, get_balance_report, get_expenses_by_categories

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
def balance_report(request: Request,
                   input_data: BalanceReportInputSchema,
                   db: Session = Depends(get_db)) -> list[dict]:
    """ Get all expenses for one account within a given time period """
    logger.info(f"Getting balance report for user_id: {request.state.user['id']}, "
                f"account_ids: {input_data.account_ids}, date: {input_data.balance_date}")
    try:
        result: list[dict] = get_balance_report(request.state.user['id'],
                                                db,
                                                [],
                                                input_data.balance_date)
        return result
    except AccessDenied as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error generting report')


@router.post('/balance/non-hidden/', response_model=list[BalanceReportOutputSchema])
def balance_report_non_hidden(request: Request,
                              input_data: BalanceReportInputSchema,
                              db: Session = Depends(get_db)) -> list[dict]:
    """ Get all expenses for one account within a given time period """
    logger.info(f"Getting balance report for NON HIDDEN accounts user_id: {request.state.user['id']}, "
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


@router.post('/expenses-by-categories/', response_model=dict[int, ExpensesReportOutputItemSchema])
def expenses_by_categories(request: Request,
                           input_data: ExpensesReportInputSchema,
                           db: Session = Depends(get_db)) -> dict:
    """ Get all expenses within a given time period """
    logger.info(f"Getting expenses by categories for user_id: {request.state.user['id']}")
    try:
        result: dict = get_expenses_by_categories(request.state.user['id'],
                                                  db,
                                                  input_data.start_date,
                                                  input_data.end_date,
                                                  input_data.categories)

        return result
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error generting report')
