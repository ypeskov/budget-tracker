from datetime import date

from app.celery import celery_app
from app.database import get_db
from app.models.ExchangeRateHistory import ExchangeRateHistory
from app.services.exchange_rates import update_exchange_rates as update_exchange_rates


@celery_app.task
def send_email():
    print("Sending email...")
    return "Email sent!"


@celery_app.task
def daily_update_exchange_rates():
    db = next(get_db())

    exchange_rates: ExchangeRateHistory = update_exchange_rates(db, when=date.today())

    return exchange_rates
