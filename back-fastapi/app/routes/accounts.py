from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from icecream import ic

from app.database import get_db
from app.logger_config import logger
from app.schemas.account_schema import AccountResponseSchema, CreateAccountSchema, UpdateAccountSchema
from app.schemas.account_type_schema import AccountTypeResponseSchema
from app.dependencies.check_token import check_token
from app.services.accounts import (create_account, get_user_accounts, get_account_details, get_account_types,
                                   delete_account)
from app.services.errors import InvalidUser, InvalidCurrency, InvalidAccountType, InvalidAccount, AccessDenied
from app.models.User import User

router = APIRouter(
    tags=['Accounts'],
    prefix='/accounts',
    dependencies=[Depends(check_token)]
)


@router.post("/", response_model=AccountResponseSchema | None)
def add_account(account_dto: CreateAccountSchema, request: Request, db: Session = Depends(get_db)):
    try:
        return create_account(account_dto, request.state.user['id'], db)
    except (InvalidUser, InvalidCurrency, InvalidAccountType, InvalidAccount) as e:
        logger.exception(f'Error creating account: {e}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/', response_model=list[AccountResponseSchema] | None)
def get_accounts(request: Request, includeHidden: bool | None, db: Session = Depends(get_db)):
    try:
        return get_user_accounts(request.state.user['id'], db, include_hidden=includeHidden)
    except InvalidUser as e:
        logger.exception(f'Error getting user accounts: {e}')
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/types/', response_model=list[AccountTypeResponseSchema] | None)
def account_types(db: Session = Depends(get_db)):
    return get_account_types(db)


@router.get('/{account_id}', response_model=AccountResponseSchema | None)
def get_account_info(account_id: int,
                     request: Request,
                     db: Session = Depends(get_db)):
    try:
        return get_account_details(account_id, request.state.user['id'], db)
    except (InvalidAccount, AccessDenied) as e:
        logger.exception(f'Error getting account details: {e}')
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/{account_id}', response_model=AccountResponseSchema)
def update_account(account_id: int,
                   account_dto: UpdateAccountSchema,
                   request: Request,
                   db: Session = Depends(get_db)):
    account_dto.id = account_id
    try:
        acc = create_account(account_dto, request.state.user['id'], db)
    except (InvalidUser, InvalidCurrency, InvalidAccountType, InvalidAccount, AccessDenied) as e:
        logger.exception(f'Error updating account: {e}')
        raise HTTPException(status_code=400, detail=str(e))
    return acc


@router.delete('/{account_id}')
def delete_acc(account_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        delete_account(account_id, request.state.user['id'], db)
    except (InvalidAccount, AccessDenied) as e:
        logger.exception(f'Error getting account details: {e}')
        raise HTTPException(status_code=400, detail=str(e))

    return {'deleted': True}
