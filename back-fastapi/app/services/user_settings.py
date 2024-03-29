from sqlalchemy.orm import Session

from app.logger_config import logger
from app.models.Language import Language
from app.models.UserSettings import UserSettings


def get_languages(db: Session) -> list[Language]:
    try:
        languages: list[Language] = db.query(Language).all()
    except Exception as e:
        logger.exception(e)
        raise e

    return languages


def generate_initial_settings(user_id: int, db: Session):
    settings = {
        'language': 'en'
    }

    new_settings = UserSettings(settings=settings, user_id=user_id)
    db.add(new_settings)
    db.commit()
    db.refresh(new_settings)
    return new_settings


def get_user_settings(user_id: int, db: Session) -> UserSettings:
    try:
        user_settings: UserSettings = db.query(UserSettings).filter(UserSettings.user_id == user_id).one()
    except Exception as e:
        logger.exception(e)
        raise e

    return user_settings


def save_user_settings(user_id: int, settings: dict, db: Session) -> UserSettings:
    try:
        user_settings: UserSettings = db.query(UserSettings).filter(UserSettings.user_id == user_id).one()
        user_settings.settings = settings
        db.commit()
        db.refresh(user_settings)
    except Exception as e:
        logger.exception(e)
        raise e

    return user_settings
