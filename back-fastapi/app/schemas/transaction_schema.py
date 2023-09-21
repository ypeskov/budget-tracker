from decimal import Decimal
from datetime import datetime

from app.schemas.account_schema import AccountResponseSchema
from app.schemas.currency_schema import CurrencyResponseSchema
from app.schemas.user_schema import UserResponse
from pydantic import BaseModel


class CreateTransactionSchema(BaseModel):
    id: int | None
    account_id: int
    target_account_id: int | None
    category_id: int | None
    amount: Decimal
    target_amount: Decimal | None
    label: str = ''
    notes: str = ''
    datetime: datetime | None
    exchange_rate: Decimal | None
    is_transfer: bool
    is_income: bool


class ResponseTransactionSchema(CreateTransactionSchema):
    id: int
    user_id: int
    currency_id: int | None
    user: UserResponse
    account: AccountResponseSchema
    target_account: AccountResponseSchema | None
    currency: CurrencyResponseSchema

    class Config:
        orm_mode = True
