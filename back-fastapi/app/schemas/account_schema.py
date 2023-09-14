from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel


class AccountSchema(BaseModel):
    id: int | None
    user_id: int | None
    account_type_id: int
    currency_id: int
    balance: Decimal = 0
    name: str
    opening_date: datetime | None
    initial_balance_in_currency: Decimal | None
    opening_exchange_rate: Decimal | None
    comment: str | None
    show_in_transactions: bool = True

    class Config:
        orm_mode = True
