from sqlalchemy.orm import Session

from app.logger_config import logger
from app.models.Language import Language


def get_languages(db: Session) -> list[Language]:
    try:
        languages: list[Language] = db.query(Language).all()
    except Exception as e:
        logger.exception(e)
        raise e

    return languages
