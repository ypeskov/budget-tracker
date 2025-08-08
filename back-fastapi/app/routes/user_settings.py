from fastapi import APIRouter, Depends, Request, HTTPException, status
from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.currency_schema import CurrencyResponseSchema
from app.schemas.language_schema import LanguageSchema
from app.schemas.settings_schema import BaseCurrencyInputSchema, UserSettingsSchema
from app.services.user_settings import (
    get_languages,
    get_user_settings,
    save_user_settings,
    get_base_currency,
    update_base_currency,
)
from app.services.settings.validator import validate_settings
from app.services.settings.errors import UnknownSettingsKeyError, MissingSettingsKeyError, IncorrectSettingsTypeError
from app.services.settings.available_settings import existing_settings

ic.configureOutput(includeContext=True)

router = APIRouter(tags=['Settings'], prefix='/settings', dependencies=[Depends(check_token)])


@router.get('/languages/', response_model=list[LanguageSchema])
def get_all_languages(request: Request, db: Session = Depends(get_db)):
    """Get all languages"""
    try:
        languages = get_languages(db)
        return languages
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to get languages')


@router.get('/')
def get_settings(request: Request, db: Session = Depends(get_db)):
    """Get user settings"""
    try:
        user_settings = get_user_settings(request.state.user['id'], db)
        return user_settings
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to get user settings')


@router.post('/')
async def store_settings(request: Request, new_settings: UserSettingsSchema, db: Session = Depends(get_db)):
    """Create user settings"""
    try:
        validate_settings(existing_settings, new_settings.model_dump())
        saved_settings = save_user_settings(request.state.user['id'], new_settings.model_dump(), db)
        return saved_settings
    except UnknownSettingsKeyError as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'Unknown settings key: {e.key}')
    except MissingSettingsKeyError as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'Missing settings key: {e.key}')
    except IncorrectSettingsTypeError as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f'Incorrect settings type: {e.key}'
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to get user settings')


@router.get('/base-currency/', response_model=CurrencyResponseSchema)
async def base_currency(request: Request, db: Session = Depends(get_db)):
    """Get user base currency"""
    try:
        return get_base_currency(request.state.user['id'], db)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to get base currency')


@router.put('/base-currency/', response_model=CurrencyResponseSchema)
async def set_base_currency(request: Request, input_data: BaseCurrencyInputSchema, db: Session = Depends(get_db)):
    """Set user base currency"""
    try:
        currency_id = input_data.currency_id
        if currency_id is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='currencyId is required')
        return update_base_currency(request.state.user['id'], currency_id, db)
    except HTTPException as e:
        logger.exception(e)
        if e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='currencyId is required')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to update base currency')
