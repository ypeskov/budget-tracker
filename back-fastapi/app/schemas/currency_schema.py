from pydantic import ConfigDict, BaseModel


class CurrencyResponseSchema(BaseModel):
    id: int
    code: str
    name: str
    model_config = ConfigDict(from_attributes=True)
