from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.schemas.currency_schema import CurrencyResponseSchema
from app.services.currencies import get_user_currencies

router = APIRouter(tags=['Currencies'], prefix='/currencies', dependencies=[Depends(check_token)])


@router.get('/', response_model=list[CurrencyResponseSchema] | None)
def get_all_currencies(db: Session = Depends(get_db)):
    return get_user_currencies(db)
