from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger_config import logger
from app.schemas.account_schema import AccountResponseSchema, CreateAccountSchema, UpdateAccountSchema
from app.schemas.account_type_schema import AccountTypeResponseSchema
from app.dependencies.check_token import check_token
from app.services.accounts import create_account, get_user_accounts, \
    get_account_details, get_account_types as get_types

router = APIRouter(
    tags=['Accounts'],
    prefix='/accounts',
    dependencies=[Depends(check_token)]
)


@router.post("/", response_model=AccountResponseSchema | None)
def add_account(account_dto: CreateAccountSchema, request: Request, db: Session = Depends(get_db)):
    return create_account(account_dto, request.state.user['id'], db)


@router.get('/', response_model=list[AccountResponseSchema] | None)
def get_accounts(request: Request, db: Session = Depends(get_db)):
    return get_user_accounts(request.state.user['id'], db)


@router.get('/types/', response_model=list[AccountTypeResponseSchema] | None)
def get_account_types(db: Session = Depends(get_db)):
    return get_types(db)


@router.get('/{account_id}', response_model=AccountResponseSchema | None)
def get_account_info(account_id: int,
                     request: Request,
                     db: Session = Depends(get_db)):
    return get_account_details(account_id, request.state.user['id'], db)


@router.put('/{account_id}', response_model=AccountResponseSchema)
def update_account(account_id: int,
                   account_dto: UpdateAccountSchema,
                   request: Request,
                   db: Session = Depends(get_db)):
    account_dto.id = account_id
    try:
        acc = create_account(account_dto, request.state.user['id'], db)
    except HTTPException as e:
        logger.exception(f'Error updating account: {e.detail}')
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return acc
