import os
from pathlib import Path

from fastapi import APIRouter, Depends, Request, HTTPException, status
from icecream import ic
from sqlalchemy.orm import Session

from app.config import Settings
from app.database import get_db
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


@router.get('/backup/')
def backup_db(request: Request, db: Session = Depends(get_db)):
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
        return {'message': 'Backup of the database is successfully created'}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Unable to create a backup of the database')
