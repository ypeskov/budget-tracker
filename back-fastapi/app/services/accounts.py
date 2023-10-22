from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import asc
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from app.models.Account import Account
from app.models.AccountType import AccountType
from app.models.Currency import Currency
from app.models.User import User
from app.schemas.account_schema import CreateAccountSchema


def create_account(account_dto: CreateAccountSchema, user_id: int, db: Session = None) -> Account:
    """Create new account for user with user_id"""
    existing_user = db.query(User).filter(User.id == user_id).first()  # type: ignore
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid user")

    currency = db.query(Currency).filter_by(id=account_dto.currency_id).first()
    if not currency:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid currency")

    account_type = db.query(AccountType).filter_by(id=account_dto.account_type_id).first()
    if not account_type:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid account type")

    if account_dto.opening_date is None:
        account_dto.opening_date = datetime.utcnow()

    new_account = Account(user=existing_user, account_type=account_type, currency=currency, balance=account_dto.balance,
                          opening_date=account_dto.opening_date, is_hidden=account_dto.is_hidden, name=account_dto.name,
                          comment=account_dto.comment)
    if account_dto.id is not None:
        new_account.id = account_dto.id
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account


def get_user_accounts(user_id: int,
                      db: Session = None,
                      include_deleted: bool = False,
                      include_hidden: bool = False) -> list[Account]:
    query = db.query(Account).filter_by(user_id=user_id).order_by(asc(Account.id))

    if not include_deleted:
        query = query.filter(Account.is_deleted == False)
    if not include_hidden:
        query = query.filter(Account.is_hidden == False)

    accounts = query.all()
    return accounts


def get_account_details(account_id: int, user_id: int, db: Session = None) -> Account:
    try:
        account = db.query(Account).filter_by(id=account_id).one()
    except NoResultFound:
        raise HTTPException(404)
    if account.user_id != user_id:
        raise HTTPException(403, 'Forbidden')
    return account


def get_account_types(db: Session = None) -> list[AccountType]:
    return db.query(AccountType).all()
