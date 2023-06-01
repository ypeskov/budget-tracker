from pprint import pprint

from app.database import get_db
from app.models.DefaultCategory import DefaultCategory

db = next(get_db())


def load_default_categories():
    default_values = [
        DefaultCategory(id=1, name='Life', parent_id=None),
        DefaultCategory(id=2, name='Food', parent_id=1),
        DefaultCategory(id=3, name='Automobile', parent_id=1),
        DefaultCategory(id=4, name='Transport', parent_id=1),
        DefaultCategory(id=5, name='Housing', parent_id=1),
        DefaultCategory(id=6, name='Health', parent_id=1),
        DefaultCategory(id=7, name='Education', parent_id=1),
        DefaultCategory(id=8, name='Entertainment', parent_id=1),
        DefaultCategory(id=9, name='Finances', parent_id=1),
        DefaultCategory(id=10, name='Other', parent_id=1),
        DefaultCategory(id=11, name='Salary', parent_id=1, is_income=True),
        DefaultCategory(id=12, name='Deposit', parent_id=1, is_income=True),
        DefaultCategory(id=13, name='Present', parent_id=1, is_income=True),
        DefaultCategory(id=14, name='Rent', parent_id=1, is_income=True),
        DefaultCategory(id=15, name='Social', parent_id=1, is_income=True),
        DefaultCategory(id=16, name='Other', parent_id=1, is_income=True),
    ]

    try:
        db.bulk_save_objects(default_values)
        db.commit()
        print('Default categories are loaded in DB')
    except Exception as e:
        pprint(e.args)


if __name__ == '__main__':
    load_default_categories()