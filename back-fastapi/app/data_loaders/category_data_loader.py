from pprint import pprint

from app.database import get_db
from app.models.DefaultCategory import DefaultCategory

db = next(get_db())


def load_default_categories():
    default_values = [
        DefaultCategory(id=1, name='Life', parent_id=None),
        DefaultCategory(id=2, name='Food', parent_id=None),
        DefaultCategory(id=3, name='Automobile', parent_id=None),
        DefaultCategory(id=4, name='Transport', parent_id=None),
        DefaultCategory(id=5, name='Housing', parent_id=None),
        DefaultCategory(id=6, name='Health', parent_id=None),
        DefaultCategory(id=7, name='Education', parent_id=None),
        DefaultCategory(id=8, name='Entertainment', parent_id=None),
        DefaultCategory(id=9, name='Finances', parent_id=None),
        DefaultCategory(id=10, name='Other', parent_id=None),
        DefaultCategory(id=11, name='Parking', parent_id=3),
        DefaultCategory(id=12, name='Fuel', parent_id=3),
        DefaultCategory(id=13, name='Service', parent_id=3),
        DefaultCategory(id=14, name='Taxi', parent_id=4),
        DefaultCategory(id=15, name='Food', parent_id=1),


        DefaultCategory(id=16, name='Salary', parent_id=None, is_income=True),
        DefaultCategory(id=17, name='Deposit', parent_id=None, is_income=True),
        DefaultCategory(id=18, name='Present', parent_id=None, is_income=True),
        DefaultCategory(id=19, name='Rent', parent_id=None, is_income=True),
        DefaultCategory(id=20, name='Social', parent_id=None, is_income=True),
        DefaultCategory(id=21, name='Other', parent_id=None, is_income=True),
    ]

    try:
        db.bulk_save_objects(default_values)
        db.commit()
        print('Default categories are loaded in DB')
    except Exception as e:
        pprint(e.args)


if __name__ == '__main__':
    load_default_categories()