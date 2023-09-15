from pprint import pp
from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from app.models.Account import Account
from app.models.Currency import Currency
from app.models.Transaction import Transaction
from app.models.User import User
from app.schemas.transaction_schema import CreateTransactionSchema


def create_transaction(transaction_dto: CreateTransactionSchema, user_id: int,
                       db: Session = None) -> Transaction:
    transaction = Transaction(**transaction_dto.dict())
    transaction.user_id = user_id
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
