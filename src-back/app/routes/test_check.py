from pprint import pprint

from fastapi import APIRouter, Depends, HTTPException, Request
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.User import User
from app.schemas.schemas import UserRegistration, UserLoginSchema, Token, UserResponse
from app.dependencies.check_token import check_token


router = APIRouter(
    prefix='/test',
    dependencies=[Depends(check_token)]
)
pprint(router.dependencies)


@router.get('/check', name='test_check')
def test_check(request: Request):
    pprint(request.scope['state'].get('user'))
    return 'ololo'