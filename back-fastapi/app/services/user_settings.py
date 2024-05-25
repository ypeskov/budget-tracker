from sqlalchemy.orm import Session

from icecream import ic

from app.logger_config import logger
from app.models.Language import Language
from app.models.UserSettings import UserSettings
from app.models.User import User
from app.models.Currency import Currency

ic.configureOutput(includeContext=True)


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


def get_base_currency(user_id: int, db: Session):
    currency = db.query(Currency).join(User, User.base_currency_id == Currency.id).filter(User.id == user_id).one()

    return currency


def update_base_currency(user_id: int, currency_id: int, db: Session) -> Currency:
    currency = db.query(Currency).filter(Currency.id == currency_id).one()
    user = db.query(User).filter(User.id == user_id).one()
    user.base_currency_id = currency.id
    db.commit()
    db.refresh(user)

    return currency

