from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.UserCategory import UserCategory
from app.schemas.transaction_schema import CreateTransactionSchema


def process_transfer_type(transaction_dto: CreateTransactionSchema, account: Account, db: Session = None):
    """This function processes case of transfer from one account to another"""
    try:
        target_account = db.query(Account).filter_by(id=transaction_dto.target_account_id).one()
        account.balance -= transaction_dto.amount
        target_account.balance += transaction_dto.amount
    except NoResultFound:
        raise HTTPException(422, 'Invalid target account')

    return account, target_account


def process_non_transfer_type(transaction_dto: CreateTransactionSchema, account: Account, user_id: int,
                              transaction: Transaction, db: Session = None):
    """If the transaction is not transfer from one account to another then this function processes it"""
    try:
        category = db.query(UserCategory).filter_by(id=transaction_dto.category_id).one()
    except NoResultFound:
        raise HTTPException(422, 'Invalid category')
    if category.user_id != user_id:
        raise HTTPException(403, 'Forbidden')

    if transaction.is_income:
        account.balance += transaction.amount
    else:
        account.balance -= transaction.amount

    return account


def create_transaction(transaction_dto: CreateTransactionSchema, user_id: int, db: Session = None) -> Transaction:
    try:
        account = db.query(Account).filter_by(id=transaction_dto.account_id).one()
    except NoResultFound:
        raise HTTPException(422, 'Invalid account')
    if account.user_id != user_id:
        raise HTTPException(403, 'Forbidden')

    # We have almost all required fields in the request
    transaction = Transaction(**transaction_dto.dict())
    # but two more have to be added additionally to the transaction
    transaction.user_id = user_id
    transaction.currency = account.currency

    if transaction_dto.is_transfer:
        account, target_account = process_transfer_type(transaction_dto, account, db)
        db.add(target_account)
    else:
        account = process_non_transfer_type(transaction_dto, account, user_id, transaction, db)

    db.add(transaction)
    db.add(account)
    db.commit()
    db.refresh(transaction)

    return transaction


def get_transactions(user_id: int, db: Session = None):
    transactions = db.query(Transaction).filter_by(user_id=user_id).all()

    return transactions
