from pprint import pprint

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_schema import UserRegistration, UserLoginSchema, UserResponse
from app.schemas.token_schema import Token
from app.services.user.auth import create_user, get_jwt_token

router = APIRouter(
    prefix='/auth'
)


@router.post("/register", response_model=UserResponse)
def register_user(user_request: UserRegistration, db: Session = Depends(get_db)):
    return UserResponse.from_orm(create_user(user_request, db))


@router.post("/login", response_model=Token)
def login_user(user_login: UserLoginSchema, db: Session = Depends(get_db)):
    return get_jwt_token(user_login, db)
