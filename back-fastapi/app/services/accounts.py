from datetime import UTC, datetime

from icecream import ic
from sqlalchemy import asc, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models.Account import Account
from app.models.AccountType import AccountType
from app.models.Currency import Currency
from app.models.User import User
from app.schemas.account_schema import CreateAccountSchema, UpdateAccountSchema
from app.services.CurrencyProcessor import calc_amount
from app.services.errors import (
    AccessDenied,
    InvalidAccount,
    InvalidAccountType,
    InvalidCurrency,
    InvalidUser,
    NotFoundError,
)

ic.configureOutput(includeContext=True)


def create_account(
    account_dto: CreateAccountSchema | UpdateAccountSchema, user_id: int, db: Session
) -> Account:
    """Create new account for user with user_id"""
    existing_user = db.query(User).filter(User.id == user_id).first()  # type: ignore
    if not existing_user:
        raise InvalidUser()

    currency = db.execute(
        select(Currency).where(Currency.id == account_dto.currency_id)
    ).scalar_one_or_none()
    if not currency:
        raise InvalidCurrency()

    account_type = (
        db.query(AccountType).filter_by(id=account_dto.account_type_id).first()
    )
    if not account_type:
        raise InvalidAccountType()

    if account_dto.opening_date is None:
        account_dto.opening_date = datetime.now(UTC)

    if hasattr(account_dto, 'id'):
        account = db.execute(
            select(Account).where(
                Account.id == account_dto.id, Account.user_id == user_id
            )
        ).scalar_one_or_none()
        if account is None:
            raise InvalidAccount()
        if account:
            account.user = existing_user
            account.account_type = account_type
            account.currency = currency
            if account_dto.initial_balance:
                account.initial_balance = account_dto.initial_balance
            account.balance = account_dto.balance
            account.credit_limit = account_dto.credit_limit
            account.opening_date = account_dto.opening_date
            account.is_hidden = account_dto.is_hidden
            account.show_in_reports = account_dto.show_in_reports
            account.name = account_dto.name
            account.comment = account_dto.comment
    else:
        account = Account(
            user=existing_user,
            account_type=account_type,
            currency=currency,
            initial_balance=account_dto.initial_balance,
            balance=account_dto.balance,
            credit_limit=account_dto.credit_limit,
            opening_date=account_dto.opening_date,
            is_hidden=account_dto.is_hidden,
            name=account_dto.name,
            comment=account_dto.comment,
        )
    db.add(account)
    db.commit()
    db.refresh(account)

    return account


def get_user_accounts(
    user_id: int,
    db: Session,
    include_deleted: bool = False,
    include_hidden: bool = False,
    include_archived: bool = False,
    archived_only: bool = False,
) -> list[Account]:
    query = db.query(Account).filter_by(user_id=user_id).order_by(asc(Account.name))

    if archived_only:
        query = query.filter(Account.is_archived == True)
    else:
        if not include_deleted:
            query = query.filter(Account.is_deleted == False)
        if not include_archived:
            query = query.filter(Account.is_archived == False)
        if not include_hidden:
            query = query.filter(Account.is_hidden == False)

    accounts: list[Account] = query.all()  # type: ignore
    for account in accounts:
        account.balance_in_base_currency = calc_amount(
            account.balance,
            account.currency.code,
            datetime.now(UTC).date(),
            account.user.base_currency.code,
            db,
        )

    return accounts


def get_account_details(account_id: int, user_id: int, db: Session) -> Account:
    try:
        account: Account = db.query(Account).filter_by(id=account_id).one()
    except NoResultFound:
        raise NotFoundError("Account not found")
    if account.user_id != user_id:
        raise AccessDenied("Access denied")
    return account


def get_account_types(db: Session) -> list[AccountType]:
    return db.query(AccountType).all()


def delete_account(account_id: int, user_id: int, db: Session) -> Account:
    account = get_account_details(account_id, user_id, db)
    account.is_deleted = True
    db.commit()
    return account


def set_archive_status(
    account_id: int, is_archived: bool, user_id: int, db: Session
) -> bool:
    account = get_account_details(account_id, user_id, db)
    account.is_archived = is_archived
    account.archived_at = datetime.now(UTC)
    db.commit()

    return True
