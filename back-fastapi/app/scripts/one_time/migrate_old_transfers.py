from decimal import Decimal

from icecream import ic
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.Account import Account
from app.models.Transaction import Transaction

ic.configureOutput(prefix='----> ', includeContext=True)

db = next(get_db())  # pragma: no cover


def main():
    transactions: list[Transaction] = (db.query(Transaction)
                                       .filter(Transaction.is_transfer == True)
                                       .filter(Transaction.linked_transaction_id.is_(None))
                                       .options(joinedload(Transaction.account))
                                       .order_by(Transaction.id)
                                       .all())
    for transaction in transactions:
        target_account = db.get(Account, transaction.target_account_id)
        # ic(target_account)

        linked_transaction = Transaction(
            user_id=transaction.user_id,
            account_id=transaction.target_account_id,
            amount=transaction.target_amount,
            currency_id=target_account.currency_id,
            category_id=None,
            label=transaction.label,
            notes=transaction.notes,
            date_time=transaction.date_time,
            exchange_rate=None,
            is_income=not transaction.is_income,
            new_balance=Decimal(0),
            is_transfer=True,
            linked_transaction_id=transaction.id,
            target_account_id=transaction.account_id,
            target_new_balance=Decimal(0),
            target_amount=None,
            is_deleted=transaction.is_deleted,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
        )
        db.add(linked_transaction)
        db.flush()
        transaction.linked_transaction_id = linked_transaction.id
        transaction.target_amount = None
        transaction.target_new_balance = None
        transaction.target_account_id = None
        db.commit()


if __name__ == "__main__":  # pragma: no cover
    main()
