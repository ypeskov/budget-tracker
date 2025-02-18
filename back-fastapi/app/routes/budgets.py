from fastapi import APIRouter, Depends, HTTPException, status, Request
from icecream import ic
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.check_token import check_token
from app.logger_config import logger
from app.schemas.budgets_schema import NewBudgetInputSchema, BudgetSchema, EditBudgetInputSchema
from app.services.budgets import (create_new_budget, get_user_budgets, update_budget, delete_budget,
                                  archive_budget)
from app.services.errors import NotFoundError
from app.tasks.tasks import run_daily_budgets_processing

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
def get_budgets(request: Request, include: str = 'all', db: Session = Depends(get_db)):
    """ Get all budgets """
    logger.info(f"Getting all budgets for user_id: {request.state.user['id']}")

    try:
        budgets = get_user_budgets(user_id=request.state.user['id'], db=db, include=include)
        return budgets
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid include parameter')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error getting budgets')


@router.delete('/{id}/')
def delete(request: Request, id: int, db: Session = Depends(get_db)):
    """ Delete budget """
    logger.info(f"Deleting budget id: {id} for user_id: {request.state.user['id']}")
    try:
        delete_budget(user_id=request.state.user['id'], db=db, budget_id=id)
        return {"message": f"Budget with id {id} deleted"}
    except NotFoundError as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Budget not found')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error deleting budget')


@router.put('/{budget_id}/archive/')
def archive(request: Request, budget_id: int, db: Session = Depends(get_db)):
    """ Archive budget """
    logger.info(f"Archiving budget id: {budget_id} for user_id: {request.state.user['id']}")
    try:
        archive_budget(user_id=request.state.user['id'], db=db, budget_id=budget_id)
        return {"message": f"Budget with id {budget_id} archived"}
    except NotFoundError as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Budget not found')
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error archiving budget')


@router.get('/daily-processing/')
def daily_processing(request: Request):
    """ Daily processing """
    user_id = request.state.user['id']
    if user_id != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')
    
    logger.info("Daily processing")
    run_daily_budgets_processing.delay()
    return {"message": "Daily processing initiated"}
