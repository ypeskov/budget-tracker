from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel


class AccountTypeResponseSchema(BaseModel):
    id: int
    type_name: str
    is_credit: bool

    class Config:
        orm_mode = True
