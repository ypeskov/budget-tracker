from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound

from app.logger_config import logger
from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.UserCategory import UserCategory
from app.services.CurrencyProcessor import CurrencyProcessor
from app.services.transaction_management.TransactionManager import TransactionManager
from app.schemas.transaction_schema import CreateTransactionSchema, UpdateTransactionSchema


def process_transfer_type(transaction: Transaction, user_id: int, db: Session):
    """This function processes case of transfer from one account to another"""

    try:
        target_account = db.query(Account).filter_by(id=transaction.target_account_id).one()
    except NoResultFound:
        logger.error(f'Invalid target account {transaction.target_account_id}')
        raise HTTPException(422, 'Invalid target account')

    if target_account.user_id != user_id:
        logger.error(f'User {user_id} tried to update transaction {transaction.id} with not own target account ' +
                     f'{transaction.target_account_id}')
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


def process_non_transfer_type(transaction: Transaction, user_id: int, db: Session):
    """If the transaction is not transfer from one account to another then this function processes it"""

    try:
        category = db.query(UserCategory).filter_by(id=transaction.category_id).one()
    except NoResultFound:
        logger.error(f'Invalid category {transaction.category_id}')
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid category')

    if category.user_id != user_id:
        logger.error(f'User {user_id} tried to update transaction {transaction.id} with not own category ' +
                     f'{transaction.category_id}')
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Forbidden')

    if transaction.is_income:
        transaction.account.balance += transaction.amount
    else:
        transaction.account.balance -= transaction.amount

    return transaction


def create_transaction(transaction_details: CreateTransactionSchema, user_id: int, db: Session) -> Transaction:
    """ Create a new transaction for a user
    :param transaction_details: CreateTransactionSchema
    :param user_id: int
    :param db: SqlAlchemy Session
    :return: Transaction
    """

    transaction_manager: TransactionManager = TransactionManager(transaction_details, user_id, db)
    transaction: Transaction = transaction_manager.get_transaction()

    if transaction_details.is_transfer:
        transaction = process_transfer_type(transaction, user_id, db)
    else:
        transaction = process_non_transfer_type(transaction, user_id, db)

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

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
            type_filters.append(Transaction.is_transfer == True)  # noqa: E712

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
    transactions: list[Transaction] = stmt.offset(offset).limit(per_page).all()  # type: ignore

    return transactions


def get_transaction_details(transaction_id: int, user_id: int, db: Session) -> Transaction:
    try:
        transaction: Transaction = db.query(Transaction).filter_by(id=transaction_id).options(  # type: ignore
            joinedload(Transaction.user),
            joinedload(Transaction.account),
            joinedload(Transaction.target_account),
            joinedload(Transaction.currency)).one()
    except NoResultFound:
        logger.error(f'Transaction {transaction_id} not found')
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Transaction not found')

    if user_id != transaction.user_id:
        logger.error(f'User {user_id} tried to get not own transaction {transaction_id}')
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return transaction


def update(transaction_id: int, transaction_details: UpdateTransactionSchema, user_id: int, db: Session):
    """
    This function updates transaction. It is used in PUT method of /transactions/{transaction_id} endpoint
    """

    try:
        transaction: Transaction = db.query(Transaction).filter_by(id=transaction_id).one()  # type: ignore
    except NoResultFound:
        logger.error(f'Transaction {transaction_id} not found')
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Transaction not found')

    if user_id != transaction.user_id:
        logger.error(f'User {user_id} tried to update not own transaction {transaction_id}')
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Forbidden')

    if transaction_details.account_id is not None:
        try:
            account: Account = db.query(Account).filter_by(id=transaction_details.account_id).one()  # type: ignore
        except NoResultFound:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'Invalid account')
        if account.user_id != user_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, 'Forbidden')  # pragma: no cover
        transaction.account = account

    if transaction_details.target_account_id is not None:
        try:
            target_account: Account = db.query(Account).filter_by(  # type: ignore
                id=transaction_details.target_account_id).one()
        except NoResultFound:
            logger.error(f'Invalid target account {transaction_details.target_account_id}')
            raise HTTPException(status.HTTP_404_NOT_FOUND, 'Invalid target account')

        if target_account.user_id != user_id:  # pragma: no cover
            logger.error(f'User {user_id} tried to update transaction {transaction_id} with not own target account ' +
                         f'{transaction_details.target_account_id}')
            raise HTTPException(status.HTTP_403_FORBIDDEN, 'Forbidden')
        transaction.target_account_id = target_account.id

    if transaction_details.category_id is not None:
        try:
            category = db.query(UserCategory).filter_by(id=transaction_details.category_id).one()
        except NoResultFound:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'Invalid category')
        if category.user_id != user_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, 'Forbidden category')
        transaction.category = category

    if transaction_details.label is not None:
        transaction.label = transaction_details.label

    if transaction_details.date_time is not None:
        transaction.date_time = transaction_details.date_time

    if transaction_details.amount is not None:
        transaction.amount = transaction_details.amount

    if transaction_details.notes is not None:
        transaction.notes = transaction_details.notes

    # If is_transfer is True then transfer fields must be filled and vice versa
    if transaction_details.is_transfer is True:
        transaction.is_transfer = transaction_details.is_transfer
        transaction.category_id = None
    else:
        transaction.is_transfer = False
        transaction.target_account_id = None
        transaction.target_amount = None
        transaction.exchange_rate = None
        transaction.category_id = transaction_details.category_id

    if transaction_details.is_income is not None:
        transaction.is_income = transaction_details.is_income

    if transaction_details.currency_id is not None:
        transaction.currency_id = transaction_details.currency_id

    if transaction_details.target_amount is not None:
        transaction.target_amount = transaction_details.target_amount

    if transaction.is_transfer:
        transaction = process_transfer_type(transaction, user_id, db)
    else:
        transaction = process_non_transfer_type(transaction, user_id, db)

    db.add(transaction)
    db.commit()

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
