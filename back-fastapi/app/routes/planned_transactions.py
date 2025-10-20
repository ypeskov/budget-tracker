from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.planned_transaction_schema import (
    CreatePlannedTransactionSchema,
    PlannedTransactionOccurrenceSchema,
    ResponsePlannedTransactionSchema,
    UpdatePlannedTransactionSchema,
)
from app.services import planned_transactions as pt_service
from app.services.errors import AccessDenied, InvalidAccount

router = APIRouter(
    tags=['Planned Transactions'],
    prefix='/planned-transactions',
    dependencies=[Depends(check_token)],
)


@router.post('/', response_model=ResponsePlannedTransactionSchema, status_code=status.HTTP_201_CREATED)
def create_planned_transaction(
    request: Request, planned_transaction_dto: CreatePlannedTransactionSchema, db: Session = Depends(get_db)
):
    """
    Create a new planned transaction (one-time or recurring).
    """
    try:
        planned_transaction = pt_service.create_planned_transaction(
            planned_transaction_dto, request.state.user['id'], db
        )
        return planned_transaction
    except InvalidAccount as e:
        logger.error(f"Invalid account: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error creating planned transaction',
        )


@router.get('/', response_model=list[ResponsePlannedTransactionSchema])
def get_planned_transactions(
    request: Request,
    db: Session = Depends(get_db),
    account_ids: list[int] | None = Query(None),
    from_date: str | None = Query(None),
    to_date: str | None = Query(None),
    is_recurring: bool | None = Query(None),
    is_executed: bool | None = Query(None),
    is_active: bool | None = Query(None),
    include_inactive: bool = Query(False),
):
    """
    Get all planned transactions for the current user with optional filters.

    Query parameters:
    - account_ids: Filter by account IDs
    - from_date: Filter by planned date >= (ISO format)
    - to_date: Filter by planned date <= (ISO format)
    - is_recurring: Filter by recurring flag
    - is_executed: Filter by executed flag
    - is_active: Filter by active flag
    - include_inactive: Include inactive transactions (default: False)
    """
    try:
        filters = {}
        if account_ids:
            filters['account_ids'] = account_ids
        if from_date:
            filters['from_date'] = from_date
        if to_date:
            filters['to_date'] = to_date
        if is_recurring is not None:
            filters['is_recurring'] = is_recurring
        if is_executed is not None:
            filters['is_executed'] = is_executed
        if is_active is not None:
            filters['is_active'] = is_active
        if include_inactive:
            filters['include_inactive'] = include_inactive

        planned_transactions = pt_service.get_planned_transactions(request.state.user['id'], db, filters)
        return planned_transactions
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error fetching planned transactions',
        )


@router.get('/upcoming/occurrences', response_model=list[PlannedTransactionOccurrenceSchema])
def get_upcoming_occurrences(
    request: Request,
    db: Session = Depends(get_db),
    days: int = Query(30, description="Number of days to look ahead"),
    include_inactive: bool = Query(False, description="Include inactive planned transactions"),
):
    """
    Get all upcoming transaction occurrences within the specified time range.
    Expands recurring transactions into individual occurrences.
    """
    try:
        end_date = datetime.now() + timedelta(days=days)

        occurrences = pt_service.get_upcoming_occurrences(
            user_id=request.state.user['id'],
            end_date=end_date,
            include_inactive=include_inactive,
            db=db,
        )
        return occurrences
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error fetching upcoming occurrences',
        )


@router.get('/{planned_transaction_id}', response_model=ResponsePlannedTransactionSchema)
def get_planned_transaction(
    planned_transaction_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Get a specific planned transaction by ID.
    """
    try:
        planned_transaction = pt_service.get_planned_transaction_by_id(
            planned_transaction_id, request.state.user['id'], db
        )
        return planned_transaction
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Planned transaction not found',
        )
    except AccessDenied as e:
        logger.error(f"Access denied: {e}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error fetching planned transaction',
        )


@router.put('/{planned_transaction_id}', response_model=ResponsePlannedTransactionSchema)
def update_planned_transaction(
    planned_transaction_id: int,
    request: Request,
    planned_transaction_dto: UpdatePlannedTransactionSchema,
    db: Session = Depends(get_db),
):
    """
    Update a planned transaction.
    """
    try:
        planned_transaction = pt_service.update_planned_transaction(
            planned_transaction_id,
            planned_transaction_dto,
            request.state.user['id'],
            db,
        )
        return planned_transaction
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Planned transaction not found',
        )
    except AccessDenied as e:
        logger.error(f"Access denied: {e}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error updating planned transaction',
        )


@router.delete('/{planned_transaction_id}')
def delete_planned_transaction(
    planned_transaction_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Delete (soft delete) a planned transaction.
    """
    try:
        pt_service.delete_planned_transaction(planned_transaction_id, request.state.user['id'], db)
        return {'deleted': True}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Planned transaction not found',
        )
    except AccessDenied as e:
        logger.error(f"Access denied: {e}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error deleting planned transaction',
        )
