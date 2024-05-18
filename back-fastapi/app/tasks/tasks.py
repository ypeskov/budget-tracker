from datetime import date, datetime

from app.celery import celery_app
from app.database import get_db
from app.services.exchange_rates import update_exchange_rates as update_exchange_rates


@celery_app.task
def send_email():
    print("Sending email...")
    return "Email sent!"


@celery_app.task(bind=True, max_retries=24, default_retry_delay=20)
def daily_update_exchange_rates(task):
    db = next(get_db())

    try:
        update_exchange_rates(db, when=date.today())
    except Exception as e:
        raise task.retry(exc=e)

    now = datetime.now()
    print(f"Exchange rates updated at {now}")

    return f"Exchange rates updated at {now}"
