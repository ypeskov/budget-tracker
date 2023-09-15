from pprint import pp

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.account_schema import AccountSchema
from app.dependencies.check_token import check_token
from app.services.accounts import create_account, get_user_accounts, \
    get_account_details

router = APIRouter(
    prefix='/accounts',
    dependencies=[Depends(check_token)]
)


@router.post("/", response_model=AccountSchema | None)
def add_account(account_dto: AccountSchema,
                request: Request,
                db: Session = Depends(get_db)):
    return create_account(account_dto, request.state.user['id'], db)


@router.get('/', response_model=list[AccountSchema] | None)
def get_accounts(request: Request, db: Session = Depends(get_db)):
    return get_user_accounts(request.state.user['id'], db)


@router.get('/{account_id}', response_model=AccountSchema | None)
def get_account_info(account_id: int,
                     request: Request,
                     db: Session = Depends(get_db)):
    return get_account_details(account_id, request.state.user['id'], db)
