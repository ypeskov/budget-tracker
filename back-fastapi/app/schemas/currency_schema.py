from pydantic import BaseModel, ConfigDict


class CurrencyResponseSchema(BaseModel):
    id: int
    code: str
    name: str
    model_config = ConfigDict(from_attributes=True)
