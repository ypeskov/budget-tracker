from datetime import date, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, PlainSerializer
from pydantic.alias_generators import to_camel


class CashFlowReportInputSchema(BaseModel):
    start_date: datetime | None = None
    end_date: datetime | None = None
    period: str

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class ExpensesReportInputSchema(BaseModel):
    start_date: date
    end_date: date
    categories: list[int] = []
    hide_empty_categories: bool = False

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class ExpensesReportOutputItemSchema(BaseModel):
    id: int
    name: str
    parent_id: int | None = None
    parent_name: str | None = None
    total_expenses: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used='json'),
    ]
    currency_code: str | None = None
    is_parent: bool = False

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class CashFlowReportOutputSchema(BaseModel):
    currency: str
    total_income: dict[str, float]
    total_expenses: dict[str, float]
    net_flow: dict[str, float]

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class BalanceReportInputSchema(BaseModel):
    account_ids: list[int]
    balance_date: date

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )


class BalanceReportOutputSchema(BaseModel):
    account_id: int
    account_name: str
    currency_code: str
    balance: float
    base_currency_balance: float
    base_currency_code: str
    report_date: date

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )
