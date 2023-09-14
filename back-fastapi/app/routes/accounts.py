from pprint import pp
from typing import Annotated, Union

from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.account_schema import AccountSchema
from app.dependencies.check_token import check_token
from app.services.accounts import create_account

router = APIRouter(
    prefix='/accounts',
    dependencies=[Depends(check_token)]
)


@router.post("/", response_model=AccountSchema | None)
def add_account(account_dto: AccountSchema,
                request: Request,
                db: Session = Depends(get_db)):
    return create_account(account_dto, request.state.user['id'], db)


@router.get('/', response_model=list[AccountSchema])
def get_user_accounts():
    pass
