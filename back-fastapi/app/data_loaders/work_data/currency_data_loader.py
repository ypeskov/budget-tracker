from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.Currency import Currency


def load_default_currencies(db: Session | None = None):
    if db is None:
        db = next(get_db())  # pragma: no cover
    db.query(Currency).delete()
    db.commit()

    default_values = [
        Currency(id=1, code='USD', name='United States Dollar'),
        Currency(id=2, code='UAH', name='Ukrainian Hryvna'),
        Currency(id=3, code='EUR', name='Euro'),
        Currency(id=4, code='BGN', name='Bulgarian Lev'),
    ]

    try:
        db.bulk_save_objects(default_values)
        db.commit()
        print(f'Default currencies are loaded in the table [{Currency.__tablename__}]')
    except Exception as e:  # pragma: no cover
        ic(e.args)


if __name__ == '__main__':  # pragma: no cover
    load_default_currencies()
