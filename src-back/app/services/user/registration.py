from pprint import pprint

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.User import User, DEFAULT_CURRENCY_CODE
from app.models.Currency import Currency
from app.schemas.user_schema import UserRegistration, UserResponse

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT generation
SECRET_KEY = "your-secret-key"


def create_user(user_request: UserRegistration, db: Session):
    existing_user = db.query(User).filter(User.email == user_request.email).first()  # type: ignore
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    currency = db.query(Currency).filter_by(code=DEFAULT_CURRENCY_CODE).one()
    pprint(currency)

    hashed_password = pwd_context.hash(user_request.password)
    new_user = User(
        email=user_request.email,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        password_hash=hashed_password,
        base_currency=currency,
        is_active=True)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse.from_orm(new_user)
