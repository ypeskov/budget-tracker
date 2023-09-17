from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel


class CreateTransactionSchema(BaseModel):
    account_id: int
    target_account_id: int | None
    category_id: int | None
    amount: Decimal
    target_amount: Decimal | None
    label: str = ''
    notes: str = ''
    datetime: datetime | None
    exchange_rate: Decimal | None
    is_transfer: bool
    is_income: bool


class ResponseTransactionSchema(CreateTransactionSchema):
    id: int
    user_id: int
    currency_id: int | None
