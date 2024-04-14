from datetime import datetime

from pydantic import ConfigDict, BaseModel
from pydantic.alias_generators import to_camel


class FlowOneAccountInputSchema(BaseModel):
    account_id: int
    start_date: datetime | None = None
    end_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True,
                              alias_generator=to_camel)


class FlowOneAccountOutputSchema(BaseModel):
    total_income: float
    total_expenses: float
    net_flow: float

    model_config = ConfigDict(from_attributes=True,
                              populate_by_name=True,
                              alias_generator=to_camel)
