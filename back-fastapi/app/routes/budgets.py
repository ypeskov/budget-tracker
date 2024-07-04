from fastapi import APIRouter, Depends, HTTPException, status, Request
from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.budgets_schema import NewBudgetInputSchema, BudgetSchema, EditBudgetInputSchema
from app.services.budgets import create_new_budget, get_user_budgets, update_budget

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


@router.put('/{id}/', response_model=BudgetSchema)
def update(request: Request, input_dto: EditBudgetInputSchema, db: Session = Depends(get_db)):
    """ update budget """
    logger.info(f"Editing budget id: {input_dto.id} for user_id: {request.state.user['id']}")
    try:
        budget = update_budget(user_id=request.state.user['id'],
                                   db=db,
                                   budget_dto=input_dto)
        return budget
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error updating budget')


@router.get('/', response_model=list[BudgetSchema])
def get_budgets(request: Request, db: Session = Depends(get_db)):
    """ Get all budgets """
    logger.info(f"Getting all budgets for user_id: {request.state.user['id']}")

    try:
        budgets = get_user_budgets(user_id=request.state.user['id'], db=db)
        return budgets
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error getting budgets')
