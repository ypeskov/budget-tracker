import os
from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from app.config import Settings
from app.logger_config import logger

settings = Settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_USERNAME,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    TEMPLATE_FOLDER=Path(os.getcwd()) / 'app/templates/emails',
)


async def send_html_email(subject: str,
                          recipients: list[str],
                          template_name: str,
                          template_body: dict,
                          filename: str = None):

    message = MessageSchema(subject=subject,
                            recipients=recipients,
                            template_body=template_body,
                            subtype=MessageType.html,
                            attachments=[filename] if filename else None)
    logger.info(f'Sending backup file {filename} to {recipients}...')

    fm = FastMail(conf)
    await fm.send_message(message, template_name=template_name)

    return True
