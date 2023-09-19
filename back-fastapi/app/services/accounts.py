from pprint import pp
from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from app.models.Account import Account
from app.models.AccountType import AccountType
from app.models.Currency import Currency
from app.models.User import User
from app.schemas.account_schema import AccountResponseSchema


def create_account(account_dto: AccountResponseSchema, user_id: int,
                   db: Session = None) -> Account:
    existing_user = db.query(User).filter(
        User.id == user_id).first()  # type: ignore
    if not existing_user:
        raise HTTPException(status_code=422, detail="Invalid user")
    currency = db.query(Currency).filter_by(id=account_dto.currency_id).first()
    if not currency:
        raise HTTPException(status_code=422, detail="Invalid currency")
    account_type = db.query(AccountType).filter_by(
        id=account_dto.account_type_id).first()
    if not account_type:
        raise HTTPException(status_code=422, detail="Invalid account type")

    new_account = Account(user=existing_user, account_type=account_type,
                          currency=currency, balance=account_dto.balance,
                          opening_date=account_dto.opening_date,
                          is_hidden=account_dto.is_hidden,
                          name=account_dto.name, comment=account_dto.comment)
    db.add(new_account)
    db.commit()

    return new_account


def get_user_accounts(user_id: int,
                      db: Session = None,
                      include_deleted: bool = False,
                      include_hidden: bool = False) -> list[Type[Account]]:
    query = db.query(Account).filter_by(user_id=user_id)

    if not include_deleted:
        query = query.filter(Account.is_deleted == False)
    if not include_hidden:
        query = query.filter(Account.is_hidden == False)

    accounts = query.all()
    return accounts


def get_account_details(account_id: int, user_id: int, db: Session = None) -> \
        Type[Account]:
    try:
        account = db.query(Account).filter_by(id=account_id).one()
    except NoResultFound:
        raise HTTPException(404)
    if account.user_id != user_id:
        raise HTTPException(403, 'Forbidden')
    return account
