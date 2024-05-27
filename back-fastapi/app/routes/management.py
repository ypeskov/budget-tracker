import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from icecream import ic

from app.config import Settings
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.utils.db.backup import backup_postgres_db

ic.configureOutput(includeContext=True)

settings = Settings()

router = APIRouter(
    tags=['Management'],
    prefix='/management',
    dependencies=[Depends(check_token)]
)

conf = ConnectionConfig(
    MAIL_USERNAME="yuriy.peskov@gmail.com",
    MAIL_PASSWORD="qdno gztk dgaa rxpv",
    MAIL_FROM="yuriy.peskov@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="OrgFin.run",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(os.getcwd()) / 'templates/emails',
)


async def simple_send():
    message = MessageSchema(subject="Fastapi-Mail module",
                            recipients=["yura@peskov.in.ua", ],
                            template_body={
                                "env_name": "dev",
                                "db_name": settings.DB_NAME,
                            },
                            subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message, template_name="backup_created.html")

    return True


@router.get('/backup/')
async def backup_db():
    """ Create a backup of the database """
    logger.info('Backup of the database is requested')
    base_dir = Path(os.getcwd())
    backup_dir = base_dir / settings.DB_BACKUP_DIR

    environment = settings.ENVIRONMENT

    try:
        backup_postgres_db(env_name=environment,
                           host=settings.DB_HOST,
                           port=settings.DB_PORT,
                           dbname=settings.DB_NAME,
                           user=settings.DB_USER,
                           password=settings.DB_PASSWORD,
                           backup_dir=backup_dir)

        await simple_send()

        return {'message': 'Backup of the database is successfully created'}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Unable to create a backup of the database')
