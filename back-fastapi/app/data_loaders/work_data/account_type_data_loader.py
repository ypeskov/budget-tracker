from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.AccountType import AccountType

default_db = next(get_db())


def load_default_account_types(db: Session = None):
    if db is None:
        db = default_db
    db.query(AccountType).delete()
    db.commit()

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
        print(f'Default account types are loaded in the table [{AccountType.__tablename__}]')
    except Exception as e:
        ic(e)


if __name__ == '__main__':
    load_default_account_types()
