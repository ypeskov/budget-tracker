from app.database import get_db
from app.models.AccountType import AccountType

db = next(get_db())


def load_default_account_types():
    default_values = [
        AccountType(id=1, type_name='cash', is_credit=False),
        AccountType(id=2, type_name='regular_bank', is_credit=False),
        AccountType(id=3, type_name='debit_card', is_credit=False),
        AccountType(id=4, type_name='credit_card', is_credit=True),
        AccountType(id=5, type_name='loan', is_credit=True),
    ]

    try:
        db.bulk_save_objects(default_values)
        db.commit()
        print('Default account types are loaded in DB')
    except Exception as e:
        pprint(e.args)


if __name__ == '__main__':
    load_default_account_types()
