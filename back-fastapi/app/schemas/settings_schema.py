from pydantic import ConfigDict, BaseModel
from pydantic.alias_generators import to_camel


class BaseCurrencyInputSchema(BaseModel):
    currency_id: int

    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel)


class UserSettingsSchema(BaseModel):
    language: str

    model_config = ConfigDict(from_attributes=True,
                              alias_generator=to_camel)
