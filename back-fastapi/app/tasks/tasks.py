import asyncio
import os
from datetime import date, datetime, timedelta
from pathlib import Path

from app.celery import celery_app
from app.config import Settings
from app.database import get_db
from app.logger_config import logger
from app.models.ActivationToken import ActivationToken
from app.models.PlannedTransaction import PlannedTransaction
from app.models.User import User
from app.services.budgets import (
    put_outdated_budgets_to_archive,
    update_budget_with_amount,
)
from app.services.exchange_rates import update_exchange_rates as update_exchange_rates
from app.tasks.errors import BackupPostgresDbError
from app.utils.db.backup import backup_postgres_db
from app.utils.email import send_html_email
from app.utils.gdrive_backup import GoogleDriveBackup

settings = Settings()


@celery_app.task(bind=True, max_retries=24, default_retry_delay=600)
def daily_update_exchange_rates(task):
    db = next(get_db())

    try:
        update_exchange_rates(db, when=date.today())
    except Exception as e:
        raise task.retry(exc=e)

    now = datetime.now()
    send_email.delay(  # type: ignore
        subject='Exchange rates updated',
        recipients=settings.ADMINS_NOTIFICATION_EMAILS,
        template_name='exchange_rates_updated.html',
        template_body={
            'updated_at': now,
            'env_name': settings.ENVIRONMENT,
        },
    )

    return f"Exchange rates updated at {now}"


@celery_app.task(bind=True, max_retries=10, default_retry_delay=600)
def make_db_backup(task):
    logger.info('Backup of the database is requested')

    base_dir = Path(os.getcwd())
    backup_dir = base_dir / settings.DB_BACKUP_DIR

    environment = settings.ENVIRONMENT

    try:
        filename = backup_postgres_db(
            env_name=environment,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            backup_dir=backup_dir,
        )

        # Upload to Google Drive if configured
        gdrive_backup = GoogleDriveBackup()
        gdrive_upload_success = False
        if settings.GDRIVE_OAUTH_TOKEN:
            # Check if rclone is installed
            if not GoogleDriveBackup.check_rclone_installed():
                logger.warning("rclone not installed, skipping Google Drive upload")
            else:
                full_path = backup_dir / filename
                gdrive_upload_success = gdrive_backup.upload_to_gdrive(str(full_path))
                if gdrive_upload_success:
                    logger.info(f"Backup {filename} uploaded to Google Drive successfully")
                else:
                    logger.warning(f"Failed to upload backup {filename} to Google Drive")
        else:
            logger.info("GDRIVE_OAUTH_TOKEN not set, skipping Google Drive upload")

        send_email.delay(  # type: ignore
            subject='Database backup created',
            recipients=settings.ADMINS_NOTIFICATION_EMAILS,
            template_name='backup_created.html',
            template_body={
                'env_name': settings.ENVIRONMENT,
                'db_name': settings.DB_NAME,
                'gdrive_uploaded': gdrive_upload_success,
            },
            filename=filename,
        )

        return {
            'message': 'Backup of the database is successfully created',
            'gdrive_uploaded': gdrive_upload_success
        }
    except BackupPostgresDbError as e:
        logger.error(e)
        task.retry(exc=e)
    except Exception as e:
        logger.exception(e)
        task.retry(exc=e)


@celery_app.task(bind=True, max_retries=10, default_retry_delay=600)
def send_email(
    task, subject: str, recipients: list[str], template_name: str, template_body: dict, filename: str | None = None
):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(
            send_html_email(
                subject=subject,
                recipients=recipients,
                template_name=template_name,
                template_body=template_body,
                filename=filename,
            )
        )

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
        send_email.delay(  # type: ignore
            subject='Activate your account',
            recipients=[user.email],
            template_name='activation_email.html',
            template_body={
                'url': f'{settings.FRONTEND_URL}/activate',
                'first_name': user.first_name,
                'activation_token': activation_token.token,
            },
        )

        return True
    except Exception as e:
        logger.exception(e)
        task.retry(exc=e)


@celery_app.task(bind=True, max_retries=10, default_retry_delay=600)
def run_daily_budgets_processing(task):
    logger.info('Daily budgets processing is requested')

    db = next(get_db())
    try:
        put_outdated_budgets_to_archive(db)
    except Exception as e:
        logger.error(e)
        task.retry(exc=e)

    return True


@celery_app.task(bind=True, max_retries=10, default_retry_delay=30)
def run_user_budgets_update(task, user_id: int):
    logger.info(f'Updating budgets for user_id: {user_id}')

    db = next(get_db())
    try:
        update_budget_with_amount(db, user_id)
    except Exception as e:
        logger.error(e)
        task.retry(exc=e)

    return True


@celery_app.task(bind=True, max_retries=10, default_retry_delay=600)
def delete_old_activation_tokens(task):
    """Delete activation tokens older than 24 hours"""
    logger.info('Deleting old activation tokens')

    db = next(get_db())
    try:
        yesterday = datetime.now() - timedelta(days=1)
        deleted_count = db.query(ActivationToken).filter(
            ActivationToken.created_at < yesterday
        ).delete()
        db.commit()
        logger.info(f'Deleted {deleted_count} old activation tokens')
        return f'Deleted {deleted_count} tokens'
    except Exception as e:
        logger.exception(e)
        db.rollback()
        task.retry(exc=e)


@celery_app.task(bind=True, max_retries=10, default_retry_delay=600)
def process_due_planned_transactions(task):
    """
    Process planned transactions that are due today.
    This task should run daily to check for planned transactions
    that need to be executed.

    Note: This task does NOT automatically execute transactions,
    it only logs them. Auto-execution should be implemented based on
    business requirements.
    """
    logger.info('Processing due planned transactions')

    db = next(get_db())
    try:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)

        # Find planned transactions due today that haven't been executed
        due_transactions = db.query(PlannedTransaction).filter(
            PlannedTransaction.planned_date >= today,
            PlannedTransaction.planned_date < tomorrow,
            PlannedTransaction.is_executed == False,  # noqa: E712
            PlannedTransaction.is_active == True,  # noqa: E712
            PlannedTransaction.is_deleted == False  # noqa: E712
        ).all()

        logger.info(f'Found {len(due_transactions)} planned transactions due today')

        # For now, just log them. In the future, you might want to:
        # 1. Send notifications to users
        # 2. Auto-execute if configured
        # 3. Generate reports

        for pt in due_transactions:
            logger.info(
                f'Planned transaction {pt.id} is due: '
                f'User {pt.user_id}, Account {pt.account_id}, '
                f'Amount {pt.amount}, Label: {pt.label}'
            )

            # Optional: Auto-execute non-recurring transactions
            # if not pt.is_recurring:
            #     try:
            #         execute_planned_transaction(pt.id, pt.user_id, db)
            #         logger.info(f'Auto-executed planned transaction {pt.id}')
            #     except Exception as e:
            #         logger.error(f'Failed to auto-execute planned transaction {pt.id}: {e}')

        return f'Processed {len(due_transactions)} due planned transactions'
    except Exception as e:
        logger.exception(e)
        task.retry(exc=e)
