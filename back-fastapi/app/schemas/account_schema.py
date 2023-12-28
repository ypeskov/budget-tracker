from decimal import Decimal
from datetime import datetime
from typing import Annotated

from app.schemas.currency_schema import CurrencyResponseSchema
from app.schemas.account_type_schema import AccountTypeResponseSchema
from pydantic import ConfigDict, BaseModel, PlainSerializer


class CreateAccountSchema(BaseModel):
    id: int | None = None
    user_id: int | None = None
    account_type_id: int
    currency_id: int
    initial_balance: Annotated[Decimal, PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        )]
    balance: Annotated[Decimal, PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        )]
    name: str
    opening_date: datetime | None = None
    comment: str | None = None
    is_hidden: bool = False


class AccountResponseSchema(CreateAccountSchema):
    currency: CurrencyResponseSchema
    account_type: AccountTypeResponseSchema
    model_config = ConfigDict(from_attributes=True)
