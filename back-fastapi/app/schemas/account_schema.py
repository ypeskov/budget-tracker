from decimal import Decimal
from datetime import datetime
from typing import Annotated

from pydantic import ConfigDict, BaseModel, PlainSerializer, field_validator
from pydantic.alias_generators import to_camel

from app.schemas.currency_schema import CurrencyResponseSchema
from app.schemas.account_type_schema import AccountTypeResponseSchema


class CreateAccountSchema(BaseModel):
    user_id: int | None = None
    account_type_id: int
    currency_id: int
    initial_balance: Annotated[Decimal, PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        )] = Decimal(0)
    balance: Annotated[Decimal, PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        )] = Decimal(0)
    credit_limit: Annotated[Decimal, PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        )] = Decimal(0)
    name: str
    opening_date: datetime | None = None
    comment: str = ""
    is_hidden: bool = False
    show_in_reports: bool = True

    @field_validator("credit_limit", mode="before")
    def set_default_credit_limit(cls, value):
        if value is None:
            return Decimal(0)
        return value

    model_config = ConfigDict(populate_by_name=True,
                              alias_generator=to_camel)


class UpdateAccountSchema(CreateAccountSchema):
    id: int | None = None
    balance: Annotated[Decimal, PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        )]
    opening_date: datetime
    comment: str
    is_hidden: bool
    show_in_reports: bool

    model_config = ConfigDict(populate_by_name=True,
                              alias_generator=to_camel)


class AccountResponseSchema(CreateAccountSchema):
    id: int
    currency: CurrencyResponseSchema
    account_type: AccountTypeResponseSchema
    is_deleted: bool
    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True,
                              alias_generator=to_camel)
