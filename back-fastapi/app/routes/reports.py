from fastapi import APIRouter, Depends, HTTPException, status, Request
from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.reports_schema import FlowOneAccountInputSchema, FlowOneAccountOutputSchema
from app.services.errors import AccessDenied
from app.services.reports import get_account_flow

ic.configureOutput(includeContext=True)

router = APIRouter(
    tags=['Reports'],
    prefix='/reports',
    dependencies=[Depends(check_token)],
)


@router.post('/flow-one-account', response_model=FlowOneAccountOutputSchema)
def spent_one_account(request: Request,
                      input_data: FlowOneAccountInputSchema,
                      db: Session = Depends(get_db)) -> dict:
    """ Get all expenses for one account within a given time period """
    try:
        result: dict = get_account_flow(request.state.user['id'],
                                        db,
                                        input_data.account_id,
                                        input_data.start_date,
                                        input_data.end_date)
        return result
    except AccessDenied as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error generting report')
