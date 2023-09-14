from pprint import pp

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.Account import Account
from app.models.User import User
from app.schemas.account_schema import AccountSchema


import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def create_account(account_dto: AccountSchema, user: dict, db: Session = None):
    existing_user = db.query(User).filter(User.id == int(user['id'])).first()  # type: ignore
    pp(existing_user.email)
    if not user:
        raise HTTPException(status_code=422, detail="Invalid user")

    new_account = Account(user=existing_user)
