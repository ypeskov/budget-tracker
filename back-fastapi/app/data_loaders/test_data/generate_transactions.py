from decimal import Decimal, ROUND_DOWN
import random

from icecream import ic

from app.database import get_db
from app.models.User import User
from app.models.Account import Account
from app.models.UserCategory import UserCategory
from app.services.transactions import create_transaction
from app.schemas.transaction_schema import CreateTransactionSchema

db = next(get_db())


def generate_test_transactions():
    users = db.query(User).all()
    num_generated_transactions = 0
    transaction_id = 1
    try:
        for user in users:
            user_categories = db.query(UserCategory).filter(UserCategory.is_income == False,
                                                            UserCategory.user_id == user.id).all()
            user_categories_ids = [cat.id for cat in user_categories]
            user_accounts = db.query(Account).filter(Account.user_id == user.id).all()
            for user_acc in user_accounts:
                for i in range(20):
                    category_id = random.choice(user_categories_ids)
                    amount = Decimal(str(random.uniform(1, 10))).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                    label = f'Transaction-{i}'
                    notes = f'Notes for transaction-{i}'
                    transaction_dto = CreateTransactionSchema(id=transaction_id, category_id=category_id,
                                                              amount=amount, label=label, account_id=user_acc.id,
                                                              is_income=False, is_transfer=False, notes=notes)
                    transaction = create_transaction(transaction_dto, user.id, db)
                    transaction_id += 1
                    num_generated_transactions += 1
                    print(f'Generated #{num_generated_transactions}, Transaction: {transaction.id}')
    except Exception as e:
        ic(e)


if __name__ == '__main__':
    generate_test_transactions()
