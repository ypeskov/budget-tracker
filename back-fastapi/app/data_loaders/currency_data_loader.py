from pprint import pprint

from ..database import get_db
from ..models.Currency import Currency

db = next(get_db())


def load_default_currencies():
    default_values = [
        Currency(id=1, code='USD', name='United States Dollar'),
        Currency(id=2, code='UAH', name='Ukrainian Hryvna'),
        Currency(id=3, code='EUR', name='Euro'),
        Currency(id=4, code='BGN', name='Bulgarian Lev'),
    ]

    try:
        db.bulk_save_objects(default_values)
        db.commit()
        print('Default currencies are loaded in DB')
    except Exception as e:
        pprint(e.args)


if __name__ == '__main__':
    load_default_currencies()