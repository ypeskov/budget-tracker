from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from icecream import ic

from app.logger_config import logger
from app.database import get_db
from app.dependencies.check_token import check_token
from app.schemas.language_schema import LanguageSchema
from app.services.settings import get_languages

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
