from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.transaction_schema import CreateTransactionSchema, ResponseTransactionSchema
from app.dependencies.check_token import check_token
from app.services.transactions import create_transaction, get_transactions, get_transaction_details

router = APIRouter(
    prefix='/transactions',
    dependencies=[Depends(check_token)]
)


@router.post('/', response_model=ResponseTransactionSchema | None)
def add_user_transaction(transaction_dto: CreateTransactionSchema, request: Request, db: Session = Depends(get_db)):
    transaction = create_transaction(transaction_dto, request.state.user['id'], db)

    return transaction


@router.get('/', response_model=list[ResponseTransactionSchema])
def get_user_transactions(request: Request, page: int = 1, per_page: int = 20, db: Session = Depends(get_db)):
    return get_transactions(request.state.user['id'], db, page, per_page)


@router.get('/{transaction_id}', response_model=ResponseTransactionSchema)
def get_transaction(transaction_id: int, request: Request, db: Session = Depends(get_db)) -> ResponseTransactionSchema:
    return get_transaction_details(transaction_id, request.state.user['id'], db)
