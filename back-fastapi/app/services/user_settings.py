from datetime import datetime

from icecream import ic
from sqlalchemy.orm import Session, joinedload

from app.logger_config import logger
from app.models.Currency import Currency
from app.models.Language import Language
from app.models.PlannedTransaction import PlannedTransaction
from app.models.User import User
from app.models.UserSettings import UserSettings
from app.services.CurrencyProcessor import calc_amount

ic.configureOutput(includeContext=True)


def get_languages(db: Session) -> list[Language]:
    try:
        languages: list[Language] = db.query(Language).all()
    except Exception as e:
        logger.exception(e)
        raise e

    return languages


def generate_initial_settings(user_id: int, db: Session):
    settings = {'language': 'en', 'projectionEndDate': None, 'projectionPeriod': None}

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
    """
    Update user's base currency and convert all planned transactions to the new currency.

    Args:
        user_id: ID of the user
        currency_id: ID of the new base currency
        db: Database session

    Returns:
        Currency: The new base currency
    """
    new_currency = db.query(Currency).filter(Currency.id == currency_id).one()
    user = db.query(User).options(joinedload(User.base_currency)).filter(User.id == user_id).one()

    old_currency = user.base_currency

    # If currency is changing, convert all planned transactions
    if old_currency and old_currency.id != currency_id:
        logger.info(
            f"Converting planned transactions from {old_currency.code} to {new_currency.code} for user {user_id}"
        )

        # Get all non-deleted, non-executed planned transactions
        planned_transactions = (
            db.query(PlannedTransaction)
            .options(joinedload(PlannedTransaction.currency))
            .filter(
                PlannedTransaction.user_id == user_id,
                PlannedTransaction.is_deleted == False,  # noqa: E712
                PlannedTransaction.is_executed == False,  # noqa: E712
            )
            .all()
        )

        # Convert each planned transaction from old currency to new currency
        for pt in planned_transactions:
            # Convert amount from planned transaction's currency to new base currency
            converted_amount = calc_amount(
                pt.amount,
                pt.currency.code,
                datetime.now().date(),
                new_currency.code,
                db,
            )

            pt.amount = converted_amount
            pt.currency_id = currency_id

        logger.info(f"Converted {len(planned_transactions)} planned transactions to {new_currency.code}")

    # Update user's base currency
    user.base_currency_id = currency_id
    db.commit()
    db.refresh(user)

    return new_currency
