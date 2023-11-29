from decimal import Decimal
from datetime import datetime
from typing import Annotated

from app.schemas.account_schema import AccountResponseSchema
from app.schemas.currency_schema import CurrencyResponseSchema
from app.schemas.user_schema import UserResponse
from app.schemas.category_schema import ResponseCategorySchema
from pydantic import ConfigDict, BaseModel, PlainSerializer


class CreateTransactionSchema(BaseModel):
    id: int | None = None
    user_id: None = None
    currency_id: int | None = None
    account_id: int
    target_account_id: int | None = None
    category_id: int | None = None
    amount: Annotated[Decimal, PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        )]
    target_amount: Annotated[Decimal, PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        )] | None = None
    label: str = ''
    notes: str = ''
    date_time: datetime | None = None
    exchange_rate: Annotated[Decimal, PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        )] | None = None
    is_transfer: bool
    is_income: bool


class UpdateTransactionSchema(CreateTransactionSchema):
    id: int
    currency_id: int
    user_id: int


class ResponseTransactionSchema(CreateTransactionSchema):
    id: int
    user_id: int
    currency_id: int | None = None
    user: UserResponse
    account: AccountResponseSchema
    target_account: AccountResponseSchema | None = None
    currency: CurrencyResponseSchema
    category: ResponseCategorySchema | None = None

    model_config = ConfigDict(from_attributes=True)
