import os

from celery import Celery
# from celery.schedules import crontab

app = Celery(__name__)

app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_max_retries = 5

app.conf.beat_schedule = {
    "send-email-every-5-seconds": {
        "task": "app.celery.send_email",
        "schedule": 10.0,
    },
}


@app.task
def send_email():
    print("Sending email...")
    return "Email sent!"
