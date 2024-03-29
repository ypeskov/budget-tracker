from fastapi import APIRouter, Depends, Request, HTTPException, status
from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.language_schema import LanguageSchema
from app.services.user_settings import get_languages, get_user_settings, save_user_settings

ic.configureOutput(includeContext=True)

router = APIRouter(
    tags=['Settings'],
    prefix='/settings',
    dependencies=[Depends(check_token)]
)


@router.get('/languages/', response_model=list[LanguageSchema])
def get_all_languages(request: Request, db: Session = Depends(get_db)):
    """ Get all languages """
    try:
        languages = get_languages(db)
        return languages
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to get languages')


@router.get('/')
def get_settings(request: Request, db: Session = Depends(get_db)):
    """ Get user settings """
    try:
        user_settings = get_user_settings(request.state.user['id'], db)
        return user_settings
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to get user settings')


@router.post('/')
async def store_settings(request: Request, db: Session = Depends(get_db)):
    """ Create user settings """
    try:
        saved_settings = save_user_settings(request.state.user['id'],
                                            (await request.json())['settings'], db)
        return saved_settings
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to get user settings')
