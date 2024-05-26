from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from icecream import ic

from app.database import get_db
from app.logger_config import logger
from app.schemas.user_schema import UserRegistration, UserLoginSchema, UserResponse
from app.schemas.token_schema import Token
from app.dependencies.check_token import check_token
from app.services.auth import create_users, get_jwt_token
from app.services.user_settings import get_user_settings

ic.configureOutput(includeContext=True)

router = APIRouter(
    tags=['Auth'],
    prefix='/auth'
)


@router.post("/register/", response_model=UserResponse)
def register_user(user_request: UserRegistration, db: Session = Depends(get_db)):
    user = create_users(user_request, db)
    return user


@router.post("/login/", response_model=Token)
def login_user(user_login: UserLoginSchema, db: Session = Depends(get_db)):
    try:
        token: str = get_jwt_token(user_login, db)

        return token
    except HTTPException as e:
        logger.error(f"Error while logging in user: '{user_login.email}': {e.detail}")
        raise HTTPException(status_code=401, detail="Invalid credentials. See logs for details")
    except Exception as e:
        logger.exception(f"Error while logging in user: {user_login.email}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error. See logs for details")


@router.get('/profile/')
def get_profile(user=Depends(check_token), db: Session = Depends(get_db)) -> dict:
    try:
        user_settings = get_user_settings(user['id'], db)
        user['settings'] = user_settings.as_dict()['settings']

        return user
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal server error. See logs for details")

