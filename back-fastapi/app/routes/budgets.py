from fastapi import APIRouter, Depends, HTTPException, status, Request
from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.budgets_schema import NewBudgetInputSchema
from app.services.budgets import create_new_budget, get_user_budgets

ic.configureOutput(includeContext=True)

router = APIRouter(
    tags=['Budgets'],
    prefix='/budgets',
    dependencies=[Depends(check_token)],
)


@router.post('/add/')
def new_budget(request: Request, input_dto: NewBudgetInputSchema, db: Session = Depends(get_db)):
    """ Add new budget """
    logger.info(f"Adding new budget for user_id: {request.state.user['id']}")
    try:
        budget = create_new_budget(user_id=request.state.user['id'],
                                   db=db,
                                   budget_dto=input_dto)
        return budget
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error generting report')


@router.get('/')
def get_budgets(request: Request, db: Session = Depends(get_db)):
    """ Get all budgets """
    logger.info(f"Getting all budgets for user_id: {request.state.user['id']}")

    try:
        budgets = get_user_budgets(user_id=request.state.user['id'], db=db)
        return budgets
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error getting budgets')
