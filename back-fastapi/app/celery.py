import os

from celery import Celery  # type: ignore
from celery.schedules import crontab

from app.config import Settings

settings = Settings()

celery_app = Celery(__name__)

celery_app.conf.update(
    broker_url=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    result_backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
)

celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.broker_connection_max_retries = 5
celery_app.conf.beat_max_loop_interval = 300

celery_app.conf.update(
    timezone='Europe/Sofia',
    enable_utc=True,
)

celery_app.autodiscover_tasks(['app.tasks'])

update_exchange_rates_hour = settings.DAILY_UPDATE_EXCHANGE_RATES_HOUR
update_exchange_rates_minute = settings.DAILY_UPDATE_EXCHANGE_RATES_MINUTE

db_backup_hour = settings.DAILY_DB_BACKUP_HOUR
db_backup_minute = settings.DAILY_DB_BACKUP_MINUTE

budgets_processing_hour = settings.DAILY_BUDGETS_PROCESSING_HOUR
budgets_processing_minute = settings.DAILY_BUDGETS_PROCESSING_MINUTE

celery_app.conf.beat_schedule = {
    "update-exchange-rates-daily": {
        "task": "app.tasks.tasks.daily_update_exchange_rates",
        "schedule": crontab(
            hour=update_exchange_rates_hour, minute=update_exchange_rates_minute
        ),
    },
    "create-db-backup": {
        "task": "app.tasks.tasks.make_db_backup",
        "schedule": crontab(hour=db_backup_hour, minute=db_backup_minute),
    },
    "put-outdated-budgets-to-archive": {
        "task": "app.tasks.tasks.run_daily_budgets_processing",
        "schedule": crontab(
            hour=budgets_processing_hour, minute=budgets_processing_minute
        ),
    },
    "process-due-planned-transactions": {
        "task": "app.tasks.tasks.process_due_planned_transactions",
        "schedule": crontab(hour=0, minute=5),  # Daily at 00:05
    },
    "delete-old-activation-tokens": {
        "task": "app.tasks.tasks.delete_old_activation_tokens",
        "schedule": crontab(hour=2, minute=0),  # Daily at 02:00
    },
}
