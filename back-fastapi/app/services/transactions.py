from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound

from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.UserCategory import UserCategory
from app.services.CurrencyProcessor import CurrencyProcessor
from app.schemas.transaction_schema import CreateTransactionSchema


def process_transfer_type(transaction: Transaction, user_id: int, db: Session):
    """This function processes case of transfer from one account to another"""
    try:
        target_account = db.query(Account).filter_by(id=transaction.target_account_id).one()
    except NoResultFound:
        raise HTTPException(422, 'Invalid target account')
    if target_account.user_id != user_id:
        raise HTTPException(403, 'Forbidden')

    transaction.target_account = target_account
    if transaction.account.currency_id != transaction.target_account.currency_id:
        currency_processor: CurrencyProcessor = CurrencyProcessor(transaction, db)
        transaction = currency_processor.calculate_exchange_rate()
    else:
        transaction.target_amount = transaction.amount

    transaction.account.balance -= transaction.amount
    transaction.target_account.balance += transaction.target_amount

    return transaction


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


def create_transaction(transaction_dto: CreateTransactionSchema, user_id: int, db: Session) -> Transaction:
    try:
        account = db.query(Account).filter_by(id=transaction_dto.account_id).one()
    except NoResultFound:
        raise HTTPException(422, 'Invalid account')
    if account.user_id != user_id:
        raise HTTPException(403, 'Forbidden')

    # We have almost all required fields in the request
    transaction = Transaction(**transaction_dto.dict())
    transaction.account = account
    transaction.user_id = user_id
    transaction.currency = account.currency

    if transaction_dto.datetime is None:
        transaction.datetime = datetime.now(timezone.utc)

    if transaction_dto.is_transfer:
        transaction = process_transfer_type(transaction, user_id, db)
        db.add(transaction.account)
        db.add(transaction.target_account)
    else:
        account: Account = process_non_transfer_type(transaction_dto, account, user_id, transaction, db)
        db.add(account)

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


def get_transactions(user_id: int, db: Session = None):
    transactions = db.query(Transaction).options(joinedload(Transaction.account),
                                                 joinedload(Transaction.target_account),
                                                 joinedload(Transaction.category),
                                                 joinedload(Transaction.currency)).filter_by(
        user_id=user_id).all()
    return transactions
