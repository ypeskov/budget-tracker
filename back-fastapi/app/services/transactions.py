from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound

from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.UserCategory import UserCategory
from app.services.CurrencyProcessor import CurrencyProcessor
from app.schemas.transaction_schema import CreateTransactionSchema, UpdateTransactionSchema


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
                              transaction: Transaction, db: Session):
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
    transaction = Transaction(**transaction_dto.model_dump())
    transaction.account = account
    transaction.user_id = user_id
    transaction.currency = account.currency

    if transaction_dto.date_time is None:
        transaction.date_time = datetime.now(timezone.utc)

    if transaction_dto.is_transfer:
        transaction = process_transfer_type(transaction, user_id, db)
        db.add(transaction.account)
        db.add(transaction.target_account)
    else:
        account = process_non_transfer_type(transaction_dto, account, user_id, transaction, db)
        db.add(account)

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.refresh(transaction.account)
    db.refresh(transaction.user)
    db.refresh(transaction.currency)
    if transaction.target_account is not None:
        db.refresh(transaction.currency)

    return transaction


def get_transactions(user_id: int, db: Session, params={}) -> list[Transaction]:
    stmt = (db.query(Transaction).options(joinedload(Transaction.account),
                                          joinedload(Transaction.target_account),
                                          joinedload(Transaction.category),
                                          joinedload(Transaction.currency))
            .filter_by(user_id=user_id)
            .order_by(Transaction.date_time.desc()))

    if 'types' in params:
        type_filters = []
        expense_or_income = []
        if 'expense' in params['types']:
            expense_or_income.append(Transaction.is_income == False)
        if 'income' in params['types']:
            expense_or_income.append(Transaction.is_income == True)
        if len(expense_or_income) > 0:
            if 'categories' not in params:
                type_filters.append(or_(*expense_or_income))
            else:
                type_filters.append(and_(or_(*expense_or_income), Transaction.category_id.in_(params['categories'])))

        if 'transfer' in params['types']:
            type_filters.append(Transaction.is_transfer == True)

        if type_filters:
            stmt = stmt.filter(or_(*type_filters))

    if 'currencies' in params:
        stmt = stmt.filter(Transaction.currency_id.in_(params['currencies']))

    if 'accounts' in params:
        stmt = stmt.filter(
            or_(Transaction.account_id.in_(params['accounts']),
                (Transaction.target_account_id.in_(params['accounts']))))

    page = 1
    if 'page' in params:
        page = int(params['page'])
    per_page = 30
    if 'per_page' in params:
        per_page = int(params['per_page'])
    offset = (page - 1) * per_page
    transactions = stmt.offset(offset).limit(per_page).all()

    return transactions


def get_transaction_details(transaction_id: int, user_id: int, db: Session) -> Transaction:
    try:
        transaction = db.query(Transaction).filter_by(id=transaction_id).options(joinedload(Transaction.user),
                                                                                 joinedload(Transaction.account),
                                                                                 joinedload(Transaction.target_account),
                                                                                 joinedload(Transaction.currency)).one()
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Transaction not found')

    if user_id != transaction.user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return transaction


def update(transaction_id: int, transaction_details: UpdateTransactionSchema, user_id: int, db: Session):
    """
    This function updates transaction. It is used in PUT method of /transactions/{transaction_id} endpoint
    """
    try:
        transaction = db.query(Transaction).filter_by(id=transaction_id).one()
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Transaction not found')

    if user_id != transaction.user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    if transaction_details.account_id is not None:
        try:
            account = db.query(Account).filter_by(id=transaction_details.account_id).one()
        except NoResultFound:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'Invalid account')
        if account.user_id != user_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, 'Forbidden')
        transaction.account = account

    if transaction_details.target_account_id is not None:
        try:
            target_account = db.query(Account).filter_by(id=transaction_details.target_account_id).one()
        except NoResultFound:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'Invalid target account')
        if target_account.user_id != user_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, 'Forbidden')
        transaction.target_account = target_account

    if transaction_details.category_id is not None:
        try:
            category = db.query(UserCategory).filter_by(id=transaction_details.category_id).one()
        except NoResultFound:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'Invalid category')
        if category.user_id != user_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, 'Forbidden')
        transaction.category = category

    if transaction_details.date_time is not None:
        transaction.date_time = transaction_details.date_time

    if transaction_details.amount is not None:
        transaction.amount = transaction_details.amount

    if transaction_details.notes is not None:
        transaction.notes = transaction_details.notes

    if transaction_details.is_transfer is not None:
        transaction.is_transfer = transaction_details.is_transfer

    if transaction_details.is_income is not None:
        transaction.is_income = transaction_details.is_income

    if transaction_details.currency_id is not None:
        transaction.currency_id = transaction_details.currency_id

    if transaction_details.target_amount is not None:
        transaction.target_amount = transaction_details.target_amount

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.refresh(transaction.account)
    db.refresh(transaction.user)
    db.refresh(transaction.currency)

    return transaction


# def delete_transaction(transaction_id: int, user_id: int, db: Session):
#     """
#     This function deletes transaction. It is used in DELETE method of /transactions/{transaction_id} endpoint
#     """
#     try:
#         transaction = db.query(Transaction).filter_by(id=transaction_id).one()
#     except NoResultFound:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Transaction not found')
#
#     if user_id != transaction.user_id:
#         raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Forbidden')
#
#     transaction.is_deleted = True
#     db.add(transaction)
#     db.commit()
#     db.refresh(transaction)
#
#
