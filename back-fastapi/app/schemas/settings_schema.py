from pydantic import BaseModel, ConfigDict


class BaseCurrencyInputSchema(BaseModel):
    currency_id: int

    model_config = ConfigDict(from_attributes=True)


class UserSettingsSchema(BaseModel):
    language: str
    projectionEndDate: str | None = None
    projectionPeriod: str | None = None

    model_config = ConfigDict(from_attributes=True)
