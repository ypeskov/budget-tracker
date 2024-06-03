from datetime import datetime, date

from pydantic import ConfigDict, BaseModel
from pydantic.alias_generators import to_camel


class CashFlowReportInputSchema(BaseModel):
    start_date: datetime | None = None
    end_date: datetime | None = None
    period: str

    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True,
                              alias_generator=to_camel)


class CashFlowReportOutputSchema(BaseModel):
    currency: str
    total_income: dict[str, float]
    total_expenses: dict[str, float]
    net_flow: dict[str, float]

    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True,
                              alias_generator=to_camel)


class BalanceReportInputSchema(BaseModel):
    account_ids: list[int]
    balance_date: date

    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True,
                              alias_generator=to_camel)


class BalanceReportOutputSchema(BaseModel):
    account_id: int
    account_name: str
    currency_code: str
    balance: float
    base_currency_balance: float
    base_currency_code: str
    report_date: date

    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True,
                              alias_generator=to_camel)
