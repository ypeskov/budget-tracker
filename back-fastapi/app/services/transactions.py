from fastapi import HTTPException, status
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound

from app.logger_config import logger
from app.models.Transaction import Transaction
from app.services.transaction_management.TransactionManager import TransactionManager
from app.schemas.transaction_schema import UpdateTransactionSchema


def create_transaction(transaction_details: UpdateTransactionSchema, user_id: int, db: Session) -> Transaction:
    """ Create a new transaction for a user
    :param transaction_details: CreateTransactionSchema
    :param user_id: int
    :param db: SqlAlchemy Session
    :return: Transaction
    """

    transaction_manager: TransactionManager = TransactionManager(transaction_details, user_id, db)
    transaction: Transaction = transaction_manager.process().get_transaction()

    return transaction


def get_transactions(user_id: int, db: Session, params={}, include_deleted=False) -> list[Transaction]:
    stmt = (db.query(Transaction).options(joinedload(Transaction.account),
                                          joinedload(Transaction.target_account),
                                          joinedload(Transaction.category),
                                          joinedload(Transaction.currency))
            .filter_by(user_id=user_id)
            .order_by(Transaction.date_time.desc()))

    if not include_deleted:
        stmt = stmt.filter(Transaction.is_deleted == False)  # noqa: E712

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


def update(transaction_details: UpdateTransactionSchema, user_id: int, db: Session):
    """
    This function updates transaction. It is used in PUT method of /transactions/{transaction_id} endpoint
    """

    transaction_manager: TransactionManager = TransactionManager(transaction_details, user_id, db)
    transaction: Transaction = transaction_manager.process().get_transaction()

    return transaction


def delete(transaction_id: int, user_id: int, db: Session) -> Transaction:
    transaction: Transaction = db.query(Transaction).filter_by(id=transaction_id).one_or_none()  # type: ignore

    if transaction is None:
        logger.error(f'Transaction {transaction_id} not found')
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Transaction not found')

    if user_id != transaction.user_id:
        logger.error(f'User {user_id} tried to delete not own transaction {transaction_id}')
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    transaction.is_deleted = True
    transaction_manager: TransactionManager = TransactionManager(transaction, user_id, db)
    processed_transaction = transaction_manager.delete_transaction().get_transaction()

    return processed_transaction
