from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.UserCategory import UserCategory
from app.schemas.transaction_schema import CreateTransactionSchema


def create_transaction(transaction_dto: CreateTransactionSchema, user_id: int,
                       db: Session = None) -> Transaction:
    try:
        account = db.query(Account).filter_by(id=transaction_dto.account_id).one()
    except NoResultFound:
        raise HTTPException(422, 'Invalid account')
    if account.user_id != user_id:
        raise HTTPException(403, 'Forbidden')

    try:
        category = db.query(UserCategory).filter_by(id=transaction_dto.category_id).one()
    except NoResultFound:
        raise HTTPException(422, 'Invalid category')
    if category.user_id != user_id:
        raise HTTPException(403, 'Forbidden')

    transaction = Transaction(**transaction_dto.dict())
    transaction.user_id = user_id
    transaction.currency = account.currency

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction
