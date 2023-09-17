from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session
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
    currency_processor = CurrencyProcessor(transaction, db)
    currency_processor.calculate_exchange_rate()
    # amount: Decimal = transaction_dto.amount
    # if account.currency_id != target_account.currency_id and transaction_dto.exchange_rate is None:
    #     raise HTTPException(422, 'Transfer currencies are not convertable')
    # elif account.currency_id != target_account.currency_id:
    #     amount = amount * transaction_dto.exchange_rate

    # account.balance -= transaction_dto.amount
    # target_account.balance += amount

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

    if transaction_dto.is_transfer:
        transaction = process_transfer_type(transaction, user_id, db)
        db.add(transaction.target_account)
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
