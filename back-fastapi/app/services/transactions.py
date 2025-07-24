from datetime import timedelta, datetime

from fastapi import HTTPException, status
from icecream import ic
from sqlalchemy import or_, and_, delete as sa_delete
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload

from app.logger_config import logger
from app.models.Account import Account
from app.models.Transaction import Transaction
from app.models.TransactionTemplate import TransactionTemplate
from app.schemas.transaction_schema import (
    UpdateTransactionSchema,
    CreateTransactionSchema,
)
from app.services.errors import AccessDenied
from app.services.transaction_management.TransactionManager import TransactionManager
from app.services.transaction_management.errors import InvalidTransaction
from app.services.CurrencyProcessor import calc_amount

ic.configureOutput(includeContext=True)


def create_transaction(transaction_details: CreateTransactionSchema, user_id: int, db: Session) -> Transaction:
    """Create a new transaction for a user
    :param transaction_details: CreateTransactionSchema
    :param user_id: int
    :param db: SqlAlchemy Session
    :return: Transaction
    """
    transaction_manager: TransactionManager = TransactionManager(transaction_details, user_id, db)
    transaction: Transaction = transaction_manager.process().get_transaction()

    return transaction


def get_transactions(user_id: int, db: Session, params: dict | None = None, include_deleted=False) -> list[Transaction]:
    if params is None:
        params = dict()

    stmt = (
        db.query(Transaction)
        .join(Transaction.account)
        .options(joinedload(Transaction.account), joinedload(Transaction.category))
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.date_time.desc())
    )

    if not include_deleted:
        stmt = stmt.filter(Transaction.is_deleted == False)  # noqa: E712

    if "types" in params:
        type_filters = []
        expense_or_income = []
        if "expense" in params["types"]:
            expense_or_income.append(Transaction.is_income == False)  # noqa: E712
        if "income" in params["types"]:
            expense_or_income.append(Transaction.is_income == True)  # noqa: E712
        if len(expense_or_income) > 0:
            if "categories" not in params:
                type_filters.append(
                    and_(or_(*expense_or_income), Transaction.is_transfer == False)  # noqa: E712
                )  # noqa: E712
            else:
                type_filters.append(
                    and_(
                        or_(*expense_or_income),
                        Transaction.category_id.in_(params["categories"]),
                    )
                )

        if "transfer" in params["types"]:
            type_filters.append(Transaction.is_transfer == True)  # noqa: E712

        if type_filters:
            stmt = stmt.filter(or_(*type_filters))

    if "currencies" in params:
        stmt = stmt.filter(Account.currency_id.in_(params["currencies"]))

    if "accounts" in params:
        stmt = stmt.filter(Transaction.account_id.in_(params["accounts"]))

    if "from_date" in params:
        from_date = datetime.strptime(params["from_date"], "%Y-%m-%d").date()
        stmt = stmt.filter(Transaction.date_time >= from_date)

    if "to_date" in params:
        to_date = datetime.strptime(params["to_date"], "%Y-%m-%d").date()
        stmt = stmt.filter(Transaction.date_time < to_date + timedelta(days=1))

    if "categories" in params:
        stmt = stmt.filter(Transaction.category_id.in_(params["categories"]))

    page = 1
    if "page" in params:
        page = int(params["page"])
    per_page = 30
    if "per_page" in params:
        per_page = int(params["per_page"])
    offset = (page - 1) * per_page

    transactions: list[Transaction] = stmt.offset(offset).limit(per_page).all()  # type: ignore
    for transaction in transactions:
        transaction.base_currency_amount = calc_amount(
            transaction.amount,
            transaction.account.currency.code,
            transaction.date_time.date(),  # type: ignore
            transaction.user.base_currency.code,
            db,
        )
        transaction.base_currency_code = transaction.user.base_currency.code

    return transactions


def get_transaction_details(transaction_id: int, user_id: int, db: Session) -> Transaction:
    try:
        transaction: Transaction = (
            db.query(Transaction)  # type: ignore
            .filter_by(id=transaction_id)
            .options(
                joinedload(Transaction.user),
                joinedload(Transaction.linked_transaction),
                joinedload(Transaction.account),
            )
            .one()
        )
    except NoResultFound:
        logger.error(f"Transaction {transaction_id} not found")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    if user_id != transaction.user_id:
        logger.error(f"User {user_id} tried to get not own transaction {transaction_id}")
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    transaction.base_currency_amount = calc_amount(
        transaction.amount,
        transaction.account.currency.code,
        transaction.date_time.date(),  # type: ignore
        transaction.user.base_currency.code,
        db,
    )
    transaction.base_currency_code = transaction.user.base_currency.code

    return transaction


def update(transaction_details: UpdateTransactionSchema, user_id: int, db: Session):
    """
    This function updates transaction. It is used in PUT method of /transactions/{transaction_id} endpoint
    """
    transaction_manager: TransactionManager = TransactionManager(transaction_details, user_id, db)
    transaction: Transaction = transaction_manager.process().get_transaction()

    return transaction


def delete(transaction_id: int, user_id: int, db: Session) -> Transaction:
    transaction = db.execute(select(Transaction).filter_by(id=transaction_id)).scalar_one_or_none()

    if transaction is None:
        logger.error(f"Transaction {transaction_id} not found")
        raise InvalidTransaction("Transaction not found")

    if user_id != transaction.user_id:
        logger.error(f"User {user_id} tried to delete not own transaction {transaction_id}")
        raise AccessDenied()

    transaction.is_deleted = True
    transaction.is_template = False
    schema = UpdateTransactionSchema.model_validate(transaction)
    transaction_manager: TransactionManager = TransactionManager(schema, user_id, db)
    processed_transaction = transaction_manager.delete_transaction().get_transaction()

    return processed_transaction


def create_template(transaction_details: CreateTransactionSchema, user_id: int, db: Session) -> bool:
    """
    This function creates a template for a transaction
    :param transaction_details: CreateTransactionSchema
    :param user_id: int
    :param db: Session
    :return: bool
    """
    try:
        transaction_template = TransactionTemplate(
            user_id=user_id,
            label=transaction_details.label,
            category_id=transaction_details.category_id,
        )
        db.add(transaction_template)
        db.commit()
        db.refresh(transaction_template)
    except Exception as e:
        logger.error(f"Error creating template: {e}")
        return False

    return True


def get_templates(user_id: int, db: Session) -> list[TransactionTemplate]:
    """
    This function gets all templates for a user
    :param user_id: int
    :param db: Session
    :return: list[TransactionTemplate]
    """
    templates: list[TransactionTemplate] = (
        db.query(TransactionTemplate)
        .filter_by(user_id=user_id)
        .options(joinedload(TransactionTemplate.category))
        .order_by(TransactionTemplate.label)
        .all()
    )

    return templates


def delete_templates(user_id: int, db: Session, ids: list[int]) -> int:
    """
    This function deletes templates for a user in a more efficient way.
    :param user_id: int
    :param db: Session
    :param ids: list[int]
    :return: int (number of deleted rows)
    """
    logger.debug(f"Deleting templates for user {user_id} with ids {ids}")

    stmt = sa_delete(TransactionTemplate).where(TransactionTemplate.user_id == user_id, TransactionTemplate.id.in_(ids))

    result = db.execute(stmt)
    db.commit()

    logger.debug(f"Deleted {result.rowcount} templates for user {user_id}")

    return result.rowcount
