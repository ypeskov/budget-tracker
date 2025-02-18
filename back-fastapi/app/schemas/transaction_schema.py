from decimal import Decimal
from datetime import datetime
from typing import Annotated

from app.schemas.account_schema import AccountResponseSchema
from app.schemas.user_schema import UserResponse
from app.schemas.category_schema import ResponseCategorySchema
from pydantic import ConfigDict, BaseModel, PlainSerializer
from pydantic.alias_generators import to_camel


class CreateTransactionSchema(BaseModel):
    id: int | None = None
    # user_id: int | None = None
    account_id: int
    target_account_id: int | None = None
    category_id: int | None = None
    amount: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ]
    target_amount: (
        Annotated[
            Decimal,
            PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
        ]
        | None
    ) = None
    label: str = ""
    notes: str | None = ""
    date_time: datetime | None = None
    is_transfer: bool
    is_income: bool
    is_template: bool
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class UpdateTransactionSchema(CreateTransactionSchema):
    id: int
    # user_id: int
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class ResponseTransactionSchema(CreateTransactionSchema):
    id: int
    user_id: int
    user: UserResponse
    account: AccountResponseSchema
    base_currency_amount: (
        Annotated[
            Decimal,
            PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
        ]
        | None
    ) = None
    base_currency_code: str | None = None
    new_balance: (
        Annotated[
            Decimal,
            PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
        ]
        | None
    ) = None
    category: ResponseCategorySchema | None = None
    linked_transaction_id: int | None = None
    is_template: bool | None = None

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class ResponseTransactionTemplateSchema(BaseModel):
    category_id: int
    label: str

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )
