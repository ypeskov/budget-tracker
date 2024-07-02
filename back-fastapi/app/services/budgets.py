from datetime import timedelta
from decimal import Decimal

from sqlalchemy.orm import Session
from icecream import ic

from app.logger_config import logger
from app.models.Budget import Budget, PeriodEnum
from app.models.UserCategory import UserCategory
from app.schemas.budgets_schema import NewBudgetInputSchema

ic.configureOutput(includeContext=True)


def create_new_budget(user_id: int,
                      db: Session,
                      budget_dto: NewBudgetInputSchema) -> Budget:
    """ Create new budget """
    logger.info(f"Creating new budget for user_id: {user_id}, budget_dto: {budget_dto}")

    # Filter out categories that are not included in the user's categories
    user_categories = db.query(UserCategory).filter(UserCategory.user_id == user_id).all()
    included_categories = [category.id for category in user_categories if category.id in budget_dto.categories]
    included_categories_str = ",".join(map(str, included_categories))

    try:
        budget = Budget(
            user_id=user_id,
            name=budget_dto.name,
            target_amount=budget_dto.target_amount,
            period=budget_dto.period,
            repeat=budget_dto.repeat,
            start_date=budget_dto.start_date,
            end_date=budget_dto.end_date + timedelta(days=1),  # add 1 day to include the full end date
            included_categories=included_categories_str,
            comment=budget_dto.comment
        )
        db.add(budget)
        db.commit()
    except Exception as e:
        logger.exception(e)
        raise e

    db.refresh(budget)
    return budget
