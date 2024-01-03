from datetime import timedelta, datetime, UTC

import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.User import User, DEFAULT_CURRENCY_CODE
from app.models.Currency import Currency
from app.models.DefaultCategory import DefaultCategory
from app.models.UserCategory import UserCategory
from app.schemas.user_schema import UserRegistration, UserResponse, UserLoginSchema

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT generation
SECRET_KEY = "your-secret-key"

# JWT expiration time (30 minutes in this example)
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def copy_categories(default_category: DefaultCategory,
                    user_id: int,
                    db: Session,
                    parent_id: int | None = None
                    ):
    new_category = UserCategory(
        user_id=user_id,
        name=default_category.name,
        parent_id=parent_id,
        is_income=default_category.is_income
    )

    db.add(new_category)
    db.commit()

    for child in default_category.children:
        copy_categories(child, user_id, db, new_category.id)


def copy_all_categories(user_id: int, db: Session):
    root_categories = db.query(DefaultCategory).filter(
        DefaultCategory.parent_id == None).all()
    for root_category in root_categories:
        copy_categories(root_category, user_id, db, None)


def create_users(user_request: UserRegistration, db: Session):
    existing_user = db.query(User).filter(
        User.email == user_request.email).first()  # type: ignore
    if existing_user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="User with this email already exists")

    currency = db.query(Currency).filter_by(code=DEFAULT_CURRENCY_CODE).one()

    hashed_password = pwd_context.hash(user_request.password)
    new_user = User(
        email=user_request.email,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        password_hash=hashed_password,
        base_currency=currency,
        is_active=True)
    if user_request.id is not None:
        new_user.id = user_request.id
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    copy_all_categories(new_user.id, db)

    return new_user


def get_jwt_token(user_login: UserLoginSchema, db: Session):
    """
    Authenticate user and generate JWT.
    """
    user = db.query(User).filter(
        User.email == user_login.email).first()  # type: ignore
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email")

    if not pwd_context.verify(user_login.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        },
        expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


def create_access_token(data: dict, expires_delta: timedelta):
    """
    Generate JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta

    to_encode.update(
        {"exp": expire, 'exp_human': expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
