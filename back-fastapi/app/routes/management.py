import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, status
from icecream import ic

from app.config import Settings
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.tasks.tasks import send_email
from app.utils.db.backup import backup_postgres_db

ic.configureOutput(includeContext=True)

settings = Settings()

router = APIRouter(
    tags=['Management'],
    prefix='/management',
    dependencies=[Depends(check_token)]
)


@router.get('/backup/')
async def backup_db(request: Request):
    """ Create a backup of the database """
    logger.info('Backup of the database is requested')
    base_dir = Path(os.getcwd())
    backup_dir = base_dir / settings.DB_BACKUP_DIR

    environment = settings.ENVIRONMENT

    if request.state.user['email'] not in settings.ADMINS_NOTIFICATION_EMAILS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized')

    try:
        filename = backup_postgres_db(env_name=environment,
                                      host=settings.DB_HOST,
                                      port=settings.DB_PORT,
                                      dbname=settings.DB_NAME,
                                      user=settings.DB_USER,
                                      password=settings.DB_PASSWORD,
                                      backup_dir=backup_dir)

        send_email.delay(subject='Database backup created',
                         recipients=settings.ADMINS_NOTIFICATION_EMAILS,
                         template_name='backup_created.html',
                         template_body={
                             'env_name': settings.ENVIRONMENT,
                             'db_name': settings.DB_NAME,
                         },
                         filename=filename)

        return {'message': 'Backup of the database is successfully created'}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Unable to create a backup of the database')
