from icecream import ic
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from app.database import get_db


def clean_db(db: Session | None = None):
    if db is None:
        db = next(get_db())  # pragma: no cover

    meta = MetaData()
    meta.reflect(bind=db.get_bind())

    for table in reversed(meta.sorted_tables):
        print(f'Dropping table [{table}]')
        table.drop(db.get_bind(), checkfirst=True)

    db.commit()


if __name__ == '__main__':  # pragma: no cover
    clean_db()
