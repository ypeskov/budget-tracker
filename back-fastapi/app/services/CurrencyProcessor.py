from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.Transaction import Transaction


class CurrencyProcessor:
    def __init__(self, transaction: Transaction, db: Session):
        self.transaction = transaction
        self.db = db

    def calculate_exchange_rate(self):
        if self.transaction is None:
            raise HTTPException(422, 'Transaction is required')

        exchange_rate: Decimal | None = self.transaction.exchange_rate
        target_amount: Decimal | None = self.transaction.target_amount
        if exchange_rate is None and target_amount is None:
            raise HTTPException(422, 'Exchange rate or target amount are required')

        if target_amount is None:
            target_amount = self.transaction.amount * exchange_rate  # type: ignore
            self.transaction.target_amount = target_amount
        elif exchange_rate is None:
            exchange_rate = target_amount / self.transaction.amount
            self.transaction.exchange_rate = exchange_rate
        return self.transaction
