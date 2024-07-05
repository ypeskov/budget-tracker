from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import ConfigDict, BaseModel, PlainSerializer
from pydantic.alias_generators import to_camel

from app.models.Budget import PeriodEnum


class NewBudgetInputSchema(BaseModel):
    name: str
    currency_id: int
    target_amount: Decimal
    period: PeriodEnum
    repeat: bool
    start_date: datetime
    end_date: datetime
    categories: list[int]
    comment: str | None = None

    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True,
                              alias_generator=to_camel)


class EditBudgetInputSchema(NewBudgetInputSchema):
    id: int


class CurrencySchema(BaseModel):
    id: int
    code: str
    name: str


class BudgetSchema(BaseModel):
    id: int
    name: str
    currency_id: int
    target_amount: Annotated[Decimal, PlainSerializer(
        lambda x: float(x), return_type=float, when_used='json'
    )]
    collected_amount: Annotated[Decimal, PlainSerializer(
        lambda x: float(x), return_type=float, when_used='json'
    )]
    period: PeriodEnum
    repeat: bool
    start_date: datetime
    end_date: datetime
    included_categories: str
    is_archived: bool
    comment: str | None = None
    currency: CurrencySchema

    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True,
                              arbitrary_types_allowed=True,
                              alias_generator=to_camel)
