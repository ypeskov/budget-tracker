from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from app.models.Account import Account
from app.models.Transaction import Transaction


class CurrencyProcessor:
    def __init__(self, transaction: Transaction, db: Session):
        self.transaction = transaction
        self.db = db

    def calculate_exchange_rate(self):
        print(self.transaction)

    # def process_transfer_type(transaction_dto: CreateTransactionSchema, account: Account, user_id: int,
    #                           transaction: Transaction, db: Session = None):
    #
    #     amount: Decimal = transaction_dto.amount
    #     if account.currency_id != target_account.currency_id and transaction_dto.exchange_rate is None:
    #         raise HTTPException(422, 'Transfer currencies are not convertable')
    #     elif account.currency_id != target_account.currency_id:
    #         amount = amount * transaction_dto.exchange_rate
    #
    #     account.balance -= transaction_dto.amount
    #     target_account.balance += amount
    #
    #     return account, target_account
