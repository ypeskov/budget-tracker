import os

from datetime import date, datetime
from pathlib import Path

from app.celery import celery_app
from app.database import get_db
from app.config import Settings
from app.logger_config import logger
from app.services.exchange_rates import update_exchange_rates as update_exchange_rates
from app.utils.db.backup import backup_postgres_db
from app.tasks.errors import BackupPostgresDbError

settings = Settings()


@celery_app.task(bind=True, max_retries=24, default_retry_delay=600)
def daily_update_exchange_rates(task):
    db = next(get_db())

    try:
        update_exchange_rates(db, when=date.today())
    except Exception as e:
        raise task.retry(exc=e)

    now = datetime.now()
    print(f"Exchange rates updated at {now}")

    return f"Exchange rates updated at {now}"


@celery_app.task(bind=True, max_retries=10, default_retry_delay=600)
def make_db_backup(task):
    logger.info('Backup of the database is requested')

    base_dir = Path(os.getcwd())
    backup_dir = base_dir / settings.DB_BACKUP_DIR

    environment = settings.ENVIRONMENT

    try:
        backup_postgres_db(env_name=environment,
                           host=settings.DB_HOST,
                           port=settings.DB_PORT,
                           dbname=settings.DB_NAME,
                           user=settings.DB_USER,
                           password=settings.DB_PASSWORD,
                           backup_dir=backup_dir)
        return {'message': 'Backup of the database is successfully created'}
    except Exception as e:
        logger.exception(e)
        raise BackupPostgresDbError(message='Unable to create a backup of the database')
