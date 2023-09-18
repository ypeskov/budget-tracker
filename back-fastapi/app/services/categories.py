from sqlalchemy.orm import Session

from app.models.UserCategory import UserCategory


def get_user_categories(user_id: int, db: Session) -> list[UserCategory]:
    return db.query(UserCategory).filter_by(user_id=user_id).all()
