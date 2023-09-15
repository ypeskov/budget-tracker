from pprint import pp

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.transaction_schema import CreateTransactionSchema, \
    ResponseTransactionSchema
from app.dependencies.check_token import check_token
from app.services.transactions import create_transaction

router = APIRouter(
    prefix='/transactions',
    dependencies=[Depends(check_token)]
)


@router.post("/", response_model=ResponseTransactionSchema | None)
def add_account(transaction_dto: CreateTransactionSchema,
                request: Request,
                db: Session = Depends(get_db)):
    transaction = create_transaction(transaction_dto, request.state.user['id'],
                                     db)
    pp(transaction.__dict__)
    return transaction.__dict__
