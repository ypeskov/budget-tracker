from typing import Type

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.models.UserCategory import UserCategory
from app.schemas.category_schema import ResponseCategorySchema
from app.services.categories import get_user_categories

router = APIRouter(
    prefix='/categories',
    dependencies=[Depends(check_token)]
)


@router.get('/', response_model=list[ResponseCategorySchema])
def get_categories(request: Request, db: Session = Depends(get_db)) -> list[UserCategory]:
    return get_user_categories(request.state.user['id'], db)

