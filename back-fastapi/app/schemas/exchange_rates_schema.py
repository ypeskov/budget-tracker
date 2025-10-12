from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ExchangeRateSchema(BaseModel):
    id: int
    rates: dict
    actual_date: date
    base_currency_code: str

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )
