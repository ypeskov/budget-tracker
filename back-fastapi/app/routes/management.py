from fastapi import APIRouter, Depends, HTTPException, Request, status
from icecream import ic

from app.config import Settings
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.tasks.tasks import make_db_backup

ic.configureOutput(includeContext=True)

settings = Settings()

router = APIRouter(tags=['Management'], prefix='/management', dependencies=[Depends(check_token)])


@router.get('/backup/')
async def backup_db(request: Request):
    """Create a backup of the database"""
    logger.info('Backup of the database is requested')

    if request.state.user['email'] not in settings.ADMINS_NOTIFICATION_EMAILS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized')

    try:
        make_db_backup.delay()
        return {'message': 'Backup of the database is requested'}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unable to request a backup of the database'
        )
