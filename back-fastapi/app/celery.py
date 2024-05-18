import os

from celery import Celery  # type: ignore
from celery.schedules import crontab

from app.config import Settings

settings = Settings()

celery_app = Celery(__name__)

celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.broker_connection_max_retries = 5
celery_app.conf.beat_max_loop_interval = 10

celery_app.conf.update(
    timezone='Europe/Sofia',
    enable_utc=True,
)

celery_app.autodiscover_tasks(['app.tasks'])

update_exchange_rates_hour = settings.DAILY_UPDATE_EXCHANGE_RATES_HOUR
update_exchange_rates_minute = settings.DAILY_UPDATE_EXCHANGE_RATES_MINUTE

celery_app.conf.beat_schedule = {
    "update-exchange-rates-daily": {
        "task": "app.tasks.tasks.daily_update_exchange_rates",
        "schedule": crontab(hour=update_exchange_rates_hour,
                            minute=update_exchange_rates_minute),
    },
}
