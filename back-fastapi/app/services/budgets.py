from datetime import timedelta
from decimal import Decimal

from icecream import ic
from sqlalchemy.orm import Session, joinedload

from app.logger_config import logger
from app.models.Budget import Budget
from app.models.Transaction import Transaction
from app.models.UserCategory import UserCategory
from app.schemas.budgets_schema import NewBudgetInputSchema
from app.services.CurrencyProcessor import calc_amount

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
            currency_id=budget_dto.currency_id,
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
    fill_budget_with_existing_transactions(db, budget)

    return budget


def fill_budget_with_existing_transactions(db: Session, budget: Budget):
    """ Fill budget with existing transactions """
    logger.info(f"Filling budget with existing transactions for budget: {budget.id}")

    transactions = db.query(Transaction).filter(
        Transaction.user_id == budget.user_id,
        Transaction.is_deleted.is_(False),
        Transaction.is_transfer.is_(False),
        Transaction.is_income.is_(False),
        Transaction.date_time.between(budget.start_date, budget.end_date)
    ).all()

    for transaction in transactions:
        if budget.included_categories:
            included_categories = [int(category_id) for category_id in budget.included_categories.split(",")]
            if transaction.category_id not in included_categories:
                # Skip transactions that do not belong to the budget
                continue

        adjusted_amount: Decimal = calc_amount(transaction.amount,
                                               transaction.account.currency.code,
                                               transaction.date_time.date(),
                                               budget.currency.code,
                                               db)
        budget.collected_amount += adjusted_amount

    db.commit()
    logger.info(f"Filled budget with existing transactions for budget: {budget.id}")


def update_budget_with_amount(db: Session, transaction: Transaction):
    """ Update collected amount for all applicable budgets """
    logger.info(f"Updating collected amount for all applicable budgets for transaction: {transaction}")

    user_budgets = db.query(Budget).filter(Budget.user_id == transaction.user_id).all()
    for budget in user_budgets:
        if budget.included_categories:
            included_categories = [int(category_id) for category_id in budget.included_categories.split(",")]
            if transaction.category_id not in included_categories:
                # Skip budgets that do not include the transaction category
                continue

        if budget.start_date <= transaction.date_time <= budget.end_date:
            adjusted_amount: Decimal = calc_amount(transaction.amount,
                                                   transaction.account.currency.code,
                                                   transaction.date_time.date(),
                                                   budget.currency.code,
                                                   db)
            budget.collected_amount += adjusted_amount
            db.commit()
            logger.info(f"Updated collected amount for budget: {budget}")


def get_user_budgets(user_id: int, db: Session):
    """ Get all budgets for user """
    logger.info(f"Getting all budgets for user_id: {user_id}")

    budgets = (
        db.query(Budget)
        .options(joinedload(Budget.currency))
        .filter(
            Budget.user_id == user_id,
            Budget.is_deleted.is_(False),
            Budget.is_archived.is_(False)
        )
        .all()
    )

    return budgets
