from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.planned_transaction_schema import (
    BalanceProjectionRequestSchema,
    BalanceProjectionResponseSchema,
    FutureBalanceRequestSchema,
    FutureBalanceResponseSchema,
)
from app.services import financial_planning as fp_service

router = APIRouter(
    tags=['Financial Planning'],
    prefix='/financial-planning',
    dependencies=[Depends(check_token)],
)


@router.post('/future-balance', response_model=FutureBalanceResponseSchema)
def calculate_future_balance(
    request: Request,
    balance_request: FutureBalanceRequestSchema,
    db: Session = Depends(get_db),
):
    """
    Calculate projected balance on a future date considering planned transactions.

    Returns total balance in base currency and breakdown by account.
    """
    try:
        result = fp_service.calculate_future_balance(
            balance_request, request.state.user['id'], db
        )
        return result
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error calculating future balance',
        )


@router.post('/projection', response_model=BalanceProjectionResponseSchema)
def get_balance_projection(
    request: Request,
    projection_request: BalanceProjectionRequestSchema,
    db: Session = Depends(get_db),
):
    """
    Generate balance projection over a time period.

    Returns projection points with balance, income, and expenses for each period.
    Useful for visualizing balance trends over time.
    """
    try:
        result = fp_service.get_balance_projection(
            projection_request, request.state.user['id'], db
        )
        return result
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error generating balance projection',
        )
