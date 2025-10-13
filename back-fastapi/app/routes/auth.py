from fastapi import APIRouter, Depends, HTTPException, status
from google.auth.transport import requests
from google.oauth2 import id_token
from icecream import ic
from sqlalchemy.orm import Session

from app.config import Settings
from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.models.User import User
from app.schemas.oauth_schema import OAuthToken
from app.schemas.token_schema import Token
from app.schemas.user_schema import UserLoginSchema, UserRegistration, UserResponse
from app.services.auth import (
    activate_user,
    create_users,
    get_jwt_token,
    login_or_register,
)
from app.services.errors import NotFoundError, UserNotActivated
from app.services.user_settings import get_user_settings

ic.configureOutput(includeContext=True)

settings = Settings()

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID

router = APIRouter(tags=['Auth'], prefix='/auth')


@router.post("/register/", response_model=UserResponse)
def register_user(user_request: UserRegistration, db: Session = Depends(get_db)):
    user = create_users(user_request, db)
    return user


@router.post("/login/", response_model=Token)
def login_user(user_login: UserLoginSchema, db: Session = Depends(get_db)) -> Token:
    try:
        token: Token = get_jwt_token(user_login, db)

        return token
    except UserNotActivated as e:
        logger.error(f"Error while logging in user: '{user_login.email}': {e}")
        raise HTTPException(status_code=401, detail="User not activated")
    except NotFoundError as e:
        logger.error(f"Error while logging in user: '{user_login.email}': {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials or user not found")
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
        fullUser = db.query(User).filter(User.id == user['id']).one()
        user['settings'] = user_settings.as_dict()['settings']
        user['baseCurrency'] = fullUser.base_currency.code

        return user
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal server error. See logs for details")


@router.get('/activate/{token}')
def activate(token: str, db: Session = Depends(get_db)):
    try:
        activate_user(token, db)

        return True
    except HTTPException as e:
        logger.error(f"Error while activating user: {e.detail}")
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail="Token not found")
        if e.status_code == 400:
            raise HTTPException(status_code=400, detail="Token expired")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal server error. See logs for details")


@router.post('/oauth/', response_model=Token)
async def oauth(JWT: OAuthToken, db: Session = Depends(get_db)):
    payload = id_token.verify_oauth2_token(JWT.credential, requests.Request(), GOOGLE_CLIENT_ID)

    if payload['email']:
        if payload['email_verified']:
            payload['family_name'] = payload.get('family_name', '')
            try:
                token = login_or_register(payload['email'], payload['given_name'], payload['family_name'], db)
            except UserNotActivated as e:
                logger.error(f"Error while logging in user: [{payload['email']}]: {e}")
                raise HTTPException(status_code=401, detail="User not activated")
            except NotFoundError as e:
                logger.error(f"Error while logging in user: [{payload['email']}]: {e}")
                raise HTTPException(status_code=401, detail="Invalid credentials or user not found")
            except HTTPException as e:
                logger.error(f"Error while logging in user: [{payload['email']}]: {e.detail}")
                raise HTTPException(status_code=401, detail="Invalid credentials. See logs for details")
            except Exception as e:
                logger.exception(f"Error while logging in user: [{payload['email']}]: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Internal server error. See logs for details",
                )
        else:
            logger.error(f"Error while logging in user: [{payload['email']}]: Email not verified")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified")
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="No email provided")

    return token
