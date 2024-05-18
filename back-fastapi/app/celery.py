import os
import time

from celery.schedules import crontab
from celery import Celery  # type: ignore

celery_app = Celery(__name__)

celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.broker_connection_max_retries = 5

celery_app.autodiscover_tasks(['app.tasks'])

celery_app.conf.beat_schedule = {
    "update-exchange-rates-daily": {
        "task": "app.tasks.tasks.daily_update_exchange_rates",
        "schedule": crontab(hour='11', minute='00'),
    },
}
