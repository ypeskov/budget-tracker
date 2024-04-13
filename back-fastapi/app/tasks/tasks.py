from app.celery import celery_app


@celery_app.task
def send_email():
    print("Sending email...")
    return "Email sent!"

