from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger_config import logger
from app.models.Language import Language


def load_languages(db: Session | None = None):
    if db is None:
        db = next(get_db())  # pragma: no cover

    default_values = [
        {'id': 1, 'name': 'English', 'code': 'en'},
        {'id': 2, 'name': 'Русский', 'code': 'ru'},
        {'id': 3, 'name': 'Українська', 'code': 'uk'},
    ]

    try:
        for lang_data in default_values:
            # Check if a language already exists by code
            existing_lang = db.query(Language).filter_by(code=lang_data['code']).first()
            if not existing_lang:
                # Add only if it doesn't exist
                new_lang = Language(**lang_data)
                db.add(new_lang)
                logger.info(f"Added language: {lang_data['name']} ({lang_data['code']})")
            else:
                # Update the name if it changed
                if existing_lang.name != lang_data['name']:
                    existing_lang.name = lang_data['name']
                    logger.info(f"Updated language: {lang_data['name']} ({lang_data['code']})")

        db.commit()
        logger.info(f'Languages are synchronized in the table [{Language.__tablename__}]')
    except Exception as e:  # pragma: no cover
        db.rollback()
        logger.exception(e.args)


if __name__ == '__main__':  # pragma: no cover
    load_languages()
