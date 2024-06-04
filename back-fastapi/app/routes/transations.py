from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from icecream import ic

from app.logger_config import logger
from app.database import get_db
from app.schemas.transaction_schema import CreateTransactionSchema, ResponseTransactionSchema, UpdateTransactionSchema
from app.dependencies.check_token import check_token
from app.services.errors import AccessDenied, InvalidCategory, InvalidAccount
from app.services.transactions import create_transaction, get_transactions, get_transaction_details, update, delete
from app.services.transaction_management.errors import InvalidTransaction
from app.utils.sanitize_transaction_filters import prepare_filters

ic.configureOutput(includeContext=True)

router = APIRouter(
    tags=['Transactions'],
    prefix='/transactions',
    dependencies=[Depends(check_token)]
)


@router.post('/', response_model=ResponseTransactionSchema | None)
def add_user_transaction(transaction_dto: CreateTransactionSchema, request: Request, db: Session = Depends(get_db)):
    """ Add a new transaction for a user """

    try:
        transaction = create_transaction(transaction_dto, request.state.user['id'], db)
    except AccessDenied:
        logger.error(f'Access denied')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    except InvalidCategory:
        logger.error(f'Invalid category: {transaction_dto}')
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid category")
    except InvalidAccount:
        logger.error(f'Invalid account: {transaction_dto}')
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid account")
    except Exception as e:  # pragma: no cover
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to create transaction')

    return transaction


@router.get('/', response_model=list[ResponseTransactionSchema])
def get_user_transactions(request: Request, db: Session = Depends(get_db)):
    """ Get all transactions for a user """
    params = dict(request.query_params)
    prepare_filters(params)

    try:
        transactions = get_transactions(request.state.user['id'], db, dict(params))
        return transactions
    except Exception as e:  # pragma: no cover
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to get transactions')


@router.get('/{transaction_id}', response_model=ResponseTransactionSchema)
def get_transaction(transaction_id: int, request: Request, db: Session = Depends(get_db)) -> ResponseTransactionSchema:
    """ Get transaction details """
    return get_transaction_details(transaction_id, request.state.user['id'], db)


@router.put('/', response_model=ResponseTransactionSchema)
def update_transaction(transaction_details: UpdateTransactionSchema,
                       request: Request,
                       db: Session = Depends(get_db)) -> ResponseTransactionSchema:
    """ Update transaction details """
    try:
        transaction = update(transaction_details, request.state.user['id'], db)
        return transaction
    except InvalidTransaction as e:
        logger.error(f'Error updating transaction: {e.detail}')
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    except AccessDenied as e:
        logger.error(f'Error updating transaction: Access denied')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    except InvalidCategory:
        logger.error(f'Invalid category: {transaction_details}')
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid category")
    except HTTPException as e:
        logger.error(f'Error updating transaction: {e.detail}')
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.detail)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to update transaction')


@router.delete('/{transaction_id}', response_model=ResponseTransactionSchema)
def delete_transaction(transaction_id: int, request: Request,
                       db: Session = Depends(get_db)) -> ResponseTransactionSchema:
    """ Delete transaction """
    try:
        transaction = delete(transaction_id, request.state.user['id'], db)
        return ResponseTransactionSchema.validate(transaction)
    except InvalidTransaction as e:
        logger.error(f'Error deleting transaction: {e.detail}')
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    except AccessDenied as e:
        logger.error(f'Error deleting transaction: Access denied')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to delete transaction')
