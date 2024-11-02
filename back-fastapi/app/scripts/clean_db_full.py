from icecream import ic
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from app.database import get_db
from app.logger_config import logger


def clean_db(db: Session | None = None):
    logger.info('Cleaning database')

    if db is None:
        db = next(get_db())  # pragma: no cover

    meta = MetaData()
    meta.reflect(bind=db.get_bind())
    logger.info(f'Meta tables {meta.tables.keys()}')

    for table in reversed(meta.sorted_tables):
        logger.info('Dropping table [%s]', table)
        try:
            table.drop(db.get_bind(), checkfirst=True)
            logger.info(f'Table [{table}] dropped')
        except Exception as e:
            ic(e)
            logger.error('Error dropping table [%s]', table)
    try:
        db.commit()
        logger.info('Transaction committed')
    except Exception as e:
        ic(e)
        logger.error(f'Error committing transaction {e}')


if __name__ == '__main__':  # pragma: no cover
    clean_db()
