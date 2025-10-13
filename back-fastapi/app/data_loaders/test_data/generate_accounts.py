from datetime import datetime, timezone
from decimal import Decimal

from icecream import ic
from sqlalchemy import text

from app.database import get_db
from app.models.Account import AccountType
from app.models.Currency import Currency
from app.models.User import User
from app.schemas.account_schema import CreateAccountSchema
from app.services.accounts import create_account

db = next(get_db())


def generate_test_accounts():
    users = db.query(User).all()
    currencies = db.query(Currency).all()
    account_types = db.query(AccountType).all()

    # set autoincrement for transactions to 1
    sql_query = text(f"ALTER SEQUENCE accounts_id_seq RESTART WITH 1;")
    db.execute(sql_query)

    try:
        account_id = 1
        for user in users:
            for currency in currencies:
                acc_data0 = CreateAccountSchema(
                    # id=account_id,
                    user_id=user.id,
                    account_type_id=account_types[0].id,
                    currency_id=currency.id,
                    balance=Decimal(1000),
                    name=f'Acc-{currency.code}-0',
                    opening_date=datetime.now(timezone.utc),
                    is_hidden=False,
                    comment='',
                )
                acc = create_account(acc_data0, user.id, db)
                print(f'{acc.name} {acc.currency.code}-{acc.account_type.type_name} was created')
                account_id += 1
                acc_data1 = CreateAccountSchema(
                    # id=account_id,
                    user_id=user.id,
                    account_type_id=account_types[0].id,
                    currency_id=currency.id,
                    balance=Decimal(1000),
                    name=f'Acc-{currency.code}-1',
                    opening_date=datetime.now(timezone.utc),
                    is_hidden=False,
                    comment='',
                )
                acc = create_account(acc_data1, user.id, db)
                print(f'{acc.name} {acc.currency.code}-{acc.account_type.type_name} was created')
                account_id += 1
            print(f'-------- accounts for user {user.id} generated --------')

        print('All test accounts were generated')
    except Exception as e:
        import traceback

        ic(e.args)
        traceback.print_exc()


if __name__ == '__main__':
    generate_test_accounts()
