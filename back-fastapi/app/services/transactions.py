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

    # We have almost all required fields in the request
    transaction = Transaction(**transaction_dto.dict())

    # but two more have to be added additionally to the transaction
    transaction.user_id = user_id
    transaction.currency = account.currency

    if not transaction.is_transfer:
        if transaction.is_income:
            account.balance += transaction.amount
        else:
            account.balance -= transaction.amount
    else:
        # Implement logic of transfer from account to account
        pass

    db.add(transaction)
    db.add(account)
    db.commit()
    db.refresh(transaction)

    return transaction


def get_transactions(user_id: int, db: Session = None):
    transactions = db.query(Transaction).filter_by(user_id=user_id).all()

    return transactions
