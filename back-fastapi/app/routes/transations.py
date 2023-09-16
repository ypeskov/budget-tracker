from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.transaction_schema import CreateTransactionSchema, \
    ResponseTransactionSchema
from app.dependencies.check_token import check_token
from app.services.transactions import create_transaction, get_transactions

router = APIRouter(
    prefix='/transactions',
    dependencies=[Depends(check_token)]
)


@router.post('/', response_model=ResponseTransactionSchema | None)
def add_user_transaction(transaction_dto: CreateTransactionSchema, request: Request, db: Session = Depends(get_db)):
    transaction = create_transaction(transaction_dto, request.state.user['id'], db)

    return transaction.__dict__


@router.get('/')
def get_user_transactions(request: Request, db: Session = Depends(get_db)):
    return get_transactions(request.state.user['id'], db)

