from decimal import Decimal
from datetime import datetime

from app.schemas.currency_schema import CurrencyResponseSchema
from app.schemas.account_type_schema import AccountTypeResponseSchema
from pydantic import ConfigDict, BaseModel


class CreateAccountSchema(BaseModel):
    id: int | None = None
    user_id: int | None = None
    account_type_id: int
    currency_id: int
    balance: Decimal = 0
    name: str
    opening_date: datetime | None = None
    comment: str | None = None
    is_hidden: bool = False


class AccountResponseSchema(CreateAccountSchema):
    currency: CurrencyResponseSchema
    account_type: AccountTypeResponseSchema
    model_config = ConfigDict(from_attributes=True)
