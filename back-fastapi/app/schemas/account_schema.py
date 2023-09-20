from decimal import Decimal
from datetime import datetime

from app.schemas.currency_schema import CurrencyResponseSchema
from app.schemas.account_type_schema import AccountTypeResponseSchema
from pydantic import BaseModel


class AccountResponseSchema(BaseModel):
    id: int | None
    user_id: int | None
    account_type_id: int
    currency_id: int
    balance: Decimal = 0
    name: str
    opening_date: datetime | None
    comment: str | None
    is_hidden: bool = False
    currency: CurrencyResponseSchema
    account_type: AccountTypeResponseSchema

    class Config:
        orm_mode = True
