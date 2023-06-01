from datetime import timedelta, datetime
from pprint import pprint

import jwt
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.User import User, DEFAULT_CURRENCY_CODE
from app.models.Currency import Currency
from app.schemas.user_schema import UserRegistration, UserResponse, UserLoginSchema

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT generation
SECRET_KEY = "your-secret-key"

# JWT expiration time (30 minutes in this example)
ACCESS_TOKEN_EXPIRE_MINUTES = 30


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


def get_jwt_token(user_login: UserLoginSchema, db: Session = Depends(get_db)):
    """
    Authenticate user and generate JWT.
    """
    user = db.query(User).filter(User.email == user_login.email).first()  # type: ignore
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not pwd_context.verify(user_login.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={**UserResponse.from_orm(user).dict()}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(data: dict, expires_delta: timedelta):
    """
    Generate JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire, 'exp_human': expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt