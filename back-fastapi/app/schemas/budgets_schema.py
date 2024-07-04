from datetime import datetime
from decimal import Decimal

from pydantic import ConfigDict, BaseModel
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
