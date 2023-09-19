from pydantic import BaseModel

class CurrencyResponseSchema(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        orm_mode = True
