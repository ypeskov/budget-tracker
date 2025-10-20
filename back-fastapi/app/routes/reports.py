from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.reports_schema import (
    BalanceReportInputSchema,
    BalanceReportOutputSchema,
    CashFlowReportInputSchema,
    CashFlowReportOutputSchema,
    ExpensesReportInputSchema,
    ExpensesReportOutputItemSchema,
)
from app.services.errors import AccessDenied
from app.services.reports import (
    get_balance_report,
    get_cash_flows,
    get_diagram,
    get_expenses_by_categories,
    get_expenses_diagram_data,
)

ic.configureOutput(includeContext=True)

router = APIRouter(
    tags=['Reports'],
    prefix='/reports',
    dependencies=[Depends(check_token)],
)


@router.post('/cashflow/', response_model=CashFlowReportOutputSchema)
def cash_flow(
    request: Request,
    input_data: CashFlowReportInputSchema,
    db: Session = Depends(get_db),
) -> list[dict]:
    """Get all expenses for one account within a given time period"""
    logger.info(
        f"Getting cash flow report for user_id: {request.state.user['id']}, "
        f"start_date: {input_data.start_date}, "
        f"end_date: {input_data.end_date}, period: {input_data.period}"
    )
    try:
        result: list[dict] = get_cash_flows(
            request.state.user['id'],
            db,
            input_data.start_date,
            input_data.end_date,
            input_data.period,
        )
        return result
    except AccessDenied as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error generting report',
        )


@router.post('/balance/', response_model=list[BalanceReportOutputSchema])
def balance_report(
    request: Request,
    input_data: BalanceReportInputSchema,
    db: Session = Depends(get_db),
) -> list[dict]:
    """Get all expenses for one account within a given time period"""
    logger.info(
        f"Getting balance report for user_id: {request.state.user['id']}, "
        f"account_ids: {input_data.account_ids}, date: {input_data.balance_date}"
    )
    try:
        result: list[dict] = get_balance_report(request.state.user['id'], db, [], input_data.balance_date)
        return result
    except AccessDenied as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error generting report',
        )


@router.post('/balance/non-hidden/', response_model=list[BalanceReportOutputSchema])
def balance_report_non_hidden(
    request: Request,
    input_data: BalanceReportInputSchema,
    db: Session = Depends(get_db),
) -> list[dict]:
    """Get all expenses for one account within a given time period"""
    logger.info(
        f"Getting balance report for NON HIDDEN accounts user_id: {request.state.user['id']}, "
        f"account_ids: {input_data.account_ids}, date: {input_data.balance_date}"
    )
    try:
        result: list[dict] = get_balance_report(
            request.state.user['id'],
            db,
            input_data.account_ids,
            input_data.balance_date,
        )
        return result
    except AccessDenied as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error generting report',
        )


@router.post('/expenses-by-categories/', response_model=list[ExpensesReportOutputItemSchema])
def expenses_by_categories(
    request: Request,
    input_data: ExpensesReportInputSchema,
    db: Session = Depends(get_db),
) -> dict:
    """Get all expenses within a given time period"""
    logger.info(f"Getting expenses by categories for user_id: {request.state.user['id']}")
    try:
        result: dict = get_expenses_by_categories(
            request.state.user['id'],
            db,
            input_data.start_date,
            input_data.end_date,
            input_data.hide_empty_categories,
        )
        return result
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error generting report',
        )


@router.get('/diagram/{diagram_type}/{start_date}/{end_date}')
def diagram(
    request: Request,
    diagram_type: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db),
):
    user_id = request.state.user['id']
    logger.info(
        f"Getting diagram for user_id: {user_id}, diagram_type: {diagram_type},"
        f" start_date: {start_date}, end_date: {end_date}"
    )

    expenses = get_expenses_by_categories(
        user_id,
        db,
        datetime.strptime(start_date, '%Y-%m-%d').date(),
        datetime.strptime(end_date, '%Y-%m-%d').date(),
        hide_empty_categories=False,
    )
    try:
        diagramImage: dict = get_diagram(expenses, db, user_id)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error generting report',
        )

    return diagramImage


@router.post('/expenses-data/')
def expenses_data(
    request: Request,
    input_data: ExpensesReportInputSchema,
    db: Session = Depends(get_db),
):
    user_id = request.state.user['id']
    logger.info(
        f"Getting data for diagram for user_id: {user_id}, "
        f" start_date: {input_data.start_date}, end_date: {input_data.end_date}"
    )

    expenses = get_expenses_diagram_data(
        user_id,
        db,
        input_data.start_date,
        input_data.end_date,
        hide_empty_categories=False,
    )
    return expenses
