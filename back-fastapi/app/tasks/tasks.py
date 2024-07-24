import asyncio
import os
from datetime import date, datetime
from pathlib import Path

from app.celery import celery_app
from app.config import Settings
from app.database import get_db
from app.logger_config import logger
from app.models.ActivationToken import ActivationToken
from app.models.User import User
from app.services.budgets import put_outdated_budgets_to_archive
from app.services.exchange_rates import update_exchange_rates as update_exchange_rates
from app.tasks.errors import BackupPostgresDbError
from app.utils.db.backup import backup_postgres_db
from app.utils.email import send_html_email

settings = Settings()


@celery_app.task(bind=True, max_retries=24, default_retry_delay=600)
def daily_update_exchange_rates(task):
    db = next(get_db())

    try:
        update_exchange_rates(db, when=date.today())
    except Exception as e:
        raise task.retry(exc=e)

    now = datetime.now()
    send_email.delay(subject='Exchange rates updated',
                     recipients=settings.ADMINS_NOTIFICATION_EMAILS,
                     template_name='exchange_rates_updated.html',
                     template_body={
                         'updated_at': now,
                         'env_name': settings.ENVIRONMENT,
                     })

    return f"Exchange rates updated at {now}"


@celery_app.task(bind=True, max_retries=10, default_retry_delay=600)
def make_db_backup(task):
    logger.info('Backup of the database is requested')

    base_dir = Path(os.getcwd())
    backup_dir = base_dir / settings.DB_BACKUP_DIR

    environment = settings.ENVIRONMENT

    try:
        filename = backup_postgres_db(env_name=environment,
                                       host=settings.DB_HOST,
                                       port=settings.DB_PORT,
                                       dbname=settings.DB_NAME,
                                       user=settings.DB_USER,
                                       password=settings.DB_PASSWORD,
                                       backup_dir=backup_dir)

        send_email.delay(subject='Database backup created',
                         recipients=settings.ADMINS_NOTIFICATION_EMAILS,
                         template_name='backup_created.html',
                         template_body={
                             'env_name': settings.ENVIRONMENT,
                             'db_name': settings.DB_NAME,
                         },
                         filename=filename
                         )

        return {'message': 'Backup of the database is successfully created'}
    except BackupPostgresDbError as e:
        logger.error(e)
        task.retry(exc=e)
    except Exception as e:
        logger.exception(e)
        task.retry(exc=e)


@celery_app.task(bind=True, max_retries=10, default_retry_delay=600)
def send_email(task,
               subject: str,
               recipients: list[str],
               template_name: str,
               template_body: dict,
               filename: str | None = None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(send_html_email(subject=subject,
                                                recipients=recipients,
                                                template_name=template_name,
                                                template_body=template_body,
                                                filename=filename))

        return True
    except Exception as e:
        logger.exception(e)
        task.retry(exc=e)
    finally:
        loop.close()


@celery_app.task(bind=True, max_retries=10, default_retry_delay=600)
def send_activation_email(task, user_id: int):
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).one()
    activation_token = db.query(ActivationToken).filter(ActivationToken.user_id == user_id).one()

    try:
        send_email.delay(subject='Activate your account',
                         recipients=[user.email],
                         template_name='activation_email.html',
                         template_body={
                             'url': f'{settings.FRONTEND_URL}/activate',
                             'first_name': user.first_name,
                             'activation_token': activation_token.token,
                         })

        return True
    except Exception as e:
        logger.exception(e)
        task.retry(exc=e)


@celery_app.task(bind=True, max_retries=10, default_retry_delay=600)
def run_daily_budgets_processing(task):
    logger.info('Daily budgets processing is requested')

    db = next(get_db())
    put_outdated_budgets_to_archive(db)

    return True
