from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.models.Currency import Currency


def get_user_currencies(db: Session) -> list[Currency]:
    query = db.query(Currency).order_by(asc(Currency.code))
    currencies = query.all()

    return currencies
