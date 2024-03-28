from sqlalchemy.orm import Session

from icecream import ic

from app.database import get_db
from app.logger_config import logger
from app.models.Language import Language


def load_languages(db: Session | None = None):
    if db is None:
        db = next(get_db())  # pragma: no cover
    db.query(Language).delete()
    db.commit()

    default_values = [
        Language(id=1, name='English', code='en'),
        Language(id=3, name='Українська', code='uk'),
    ]

    try:
        db.bulk_save_objects(default_values)
        db.commit()
        logger.info(f'Default languages are loaded in the table [{Language.__tablename__}]')
    except Exception as e:  # pragma: no cover
        logger.exception(e.args)


if __name__ == '__main__':  # pragma: no cover
    load_languages()




