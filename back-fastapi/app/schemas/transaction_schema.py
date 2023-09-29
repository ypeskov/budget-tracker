from decimal import Decimal
from datetime import datetime

from app.schemas.account_schema import AccountResponseSchema
from app.schemas.currency_schema import CurrencyResponseSchema
from app.schemas.user_schema import UserResponse
from pydantic import ConfigDict, BaseModel


class CreateTransactionSchema(BaseModel):
    id: int | None = None
    account_id: int
    target_account_id: int | None = None
    category_id: int | None = None
    amount: Decimal
    target_amount: Decimal | None = None
    label: str = ''
    notes: str = ''
    date_time: datetime | None = None
    exchange_rate: Decimal | None = None
    is_transfer: bool
    is_income: bool


class ResponseTransactionSchema(CreateTransactionSchema):
    id: int
    user_id: int
    currency_id: int | None = None
    user: UserResponse
    account: AccountResponseSchema
    target_account: AccountResponseSchema | None = None
    currency: CurrencyResponseSchema

    model_config = ConfigDict(from_attributes=True)
