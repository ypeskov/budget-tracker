from datetime import timedelta, datetime, timezone
from decimal import Decimal

import pendulum
from icecream import ic
from sqlalchemy.orm import Session, joinedload

from app.logger_config import logger
from app.models.Budget import Budget, PeriodEnum
from app.models.Transaction import Transaction
from app.models.UserCategory import UserCategory
from app.schemas.budgets_schema import NewBudgetInputSchema, EditBudgetInputSchema
from app.services.CurrencyProcessor import calc_amount
from app.services.errors import NotFoundError, InvalidPeriod

ic.configureOutput(includeContext=True)


def create_new_budget(user_id: int,
                      db: Session,
                      budget_dto: NewBudgetInputSchema | EditBudgetInputSchema) -> Budget:
    """ Create new budget """
    logger.info(f"Creating new budget for user_id: {user_id}, budget_dto: {budget_dto}")

    # Filter out categories that are not included in the user's categories
    user_categories = db.query(UserCategory).filter(UserCategory.user_id == user_id).all()
    included_categories = [category.id for category in user_categories if category.id in budget_dto.categories]
    included_categories_str = ",".join(map(str, included_categories))

    try:
        # Check if it's an update operation
        if hasattr(budget_dto, "id") and budget_dto.id:
            budget: Budget | None = db.query(Budget).filter(Budget.id == budget_dto.id).one_or_none()
            if budget is None:
                raise NotFoundError(f"Budget with id {budget_dto.id} not found.")
            budget.collected_amount = Decimal(0)
            if budget is None:
                raise ValueError(f"Budget with id {budget_dto.id} not found.")
            logger.info(f"Updating budget with id: {budget_dto.id}")
        else:
            budget = Budget(user_id=user_id)
            logger.info("Creating a new budget")

        # Update budget fields
        budget.name = budget_dto.name
        budget.currency_id = budget_dto.currency_id
        budget.target_amount = budget_dto.target_amount
        budget.period = budget_dto.period
        budget.repeat = budget_dto.repeat
        budget.start_date = budget_dto.start_date
        budget.end_date = budget_dto.end_date + timedelta(days=1)  # add 1 day to include the full end date
        budget.included_categories = included_categories_str
        budget.comment = str(budget_dto.comment)

        db.add(budget)
        db.commit()
    except Exception as e:
        logger.exception(e)
        db.rollback()  # Rollback the transaction in case of error
        raise e

    db.refresh(budget)
    fill_budget_with_existing_transactions(db, budget)

    return budget


def update_budget(user_id: int,
                  db: Session,
                  budget_dto: NewBudgetInputSchema | EditBudgetInputSchema) -> Budget:
    """ Update budget """
    logger.info(f"Updating budget for user_id: {user_id}, budget_dto: {budget_dto.id}")  # type: ignore
    return create_new_budget(user_id, db, budget_dto)


def fill_budget_with_existing_transactions(db: Session, budget: Budget):
    """ Fill budget with existing transactions """
    logger.info(f"Filling budget with existing transactions for budget: {budget.id}")

    transactions: list[Transaction] = db.query(Transaction).filter(  # type: ignore
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

        assert transaction.date_time is not None, f"Transaction {transaction.id} has no date_time"

        adjusted_amount: Decimal = calc_amount(transaction.amount,
                                           transaction.account.currency.code,
                                           transaction.date_time.date(),
                                           budget.currency.code,
                                           db)
        budget.collected_amount += adjusted_amount

    db.commit()
    logger.info(f"Filled budget with existing transactions for budget: {budget.id}")


def update_budget_with_amount(db: Session, transaction: Transaction, adjusted_amount: Decimal):
    """ Update collected amount for all applicable budgets """
    logger.info(f"Updating collected amount for all applicable budgets for transaction: {transaction}")

    user_budgets: list[Budget] = (db.query(Budget)
                                  .filter(Budget.user_id == transaction.user_id, Budget.is_archived == False)
                                  .all())
    for budget in user_budgets:
        if budget.included_categories:
            included_categories = [int(category_id) for category_id in budget.included_categories.split(",")]
            if transaction.category_id not in included_categories:
                # Skip budgets that do not include the transaction category
                continue

        if budget.start_date <= transaction.date_time <= budget.end_date:  # type: ignore
            adjusted_amount = calc_amount(adjusted_amount,
                                          transaction.account.currency.code,
                                          transaction.date_time.date(),  # type: ignore
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
            # Budget.is_archived.is_(False)
        )
        .order_by(Budget.is_archived, Budget.end_date.asc())
        .all()
    )

    for budget in budgets:
        budget.end_date -= timedelta(days=1)  # subtract 1 day to exclude the full end date

    return budgets


def delete_budget(user_id: int, db: Session, budget_id: int):
    """ Delete budget """
    logger.info(f"Deleting budget with id: {budget_id}")

    budget = db.query(Budget).filter(Budget.id == budget_id, Budget.user_id == user_id).one_or_none()
    if budget is None:
        raise NotFoundError(f"Budget with id {budget_id} not found.")

    budget.is_deleted = True
    db.commit()
    db.refresh(budget)
    logger.info(f"Deleted budget with id: {budget_id}")

    return budget


def archive_budget(user_id: int, db: Session, budget_id: int):
    """ Archive budget """
    logger.info(f"Archiving budget with id: {budget_id}")

    budget = db.query(Budget).filter(Budget.id == budget_id, Budget.user_id == user_id).one_or_none()
    if budget is None:
        logger.error(f"Budget with id {budget_id} not found for user_id: {user_id}")
        raise NotFoundError(f"Budget with id {budget_id} not found.")

    budget.is_archived = True
    db.commit()
    db.refresh(budget)
    logger.info(f"Archived budget with id: {budget_id}")

    return budget


def put_outdated_budgets_to_archive(db: Session):
    """ Put budget to archive """
    logger.info("Putting outdated budgets to archive")

    now = datetime.now(timezone.utc)
    logger.info(f"Now: {now}")
    outdated_budgets: list[Budget] = (
        db.query(Budget).filter(Budget.end_date < now, Budget.is_archived.is_(False)).all())
    logger.info(f"Outdated budgets: {outdated_budgets}")
    archiving_budgets = []
    for budget in outdated_budgets:
        if budget.repeat:
            create_copy_of_outdated_budget(db, budget)
        budget.is_archived = True
        db.commit()
        archiving_budgets.append(budget.id)

    logger.info(f"Archived budgets: {archiving_budgets}")

    return archiving_budgets


def create_copy_of_outdated_budget(db: Session, budget: Budget):
    """ Create copy of outdated budget """
    logger.info(f"Creating copy of outdated budget: {budget.id}")

    end_date = pendulum.instance(budget.end_date)

    if budget.period == PeriodEnum.DAILY:
        new_start_date = end_date
        new_end_date = end_date.add(days=1)
    elif budget.period == PeriodEnum.WEEKLY:
        new_start_date = end_date
        new_end_date = end_date.add(weeks=1)
    elif budget.period == PeriodEnum.MONTHLY:
        new_start_date = end_date
        new_end_date = end_date.add(months=1)
    elif budget.period == PeriodEnum.YEARLY:
        new_start_date = end_date
        new_end_date = end_date.add(years=1)
    else:
        raise InvalidPeriod(f"Invalid period: {budget.period}")

    new_budget = Budget(
        user_id=budget.user_id,
        name=f"{budget.name} (copy)",
        currency_id=budget.currency_id,
        target_amount=budget.target_amount,
        period=budget.period,
        repeat=budget.repeat,
        start_date=new_start_date,
        end_date=new_end_date,
        included_categories=budget.included_categories,
        comment=budget.comment,
        is_deleted=False,
        is_archived=False,
        collected_amount=Decimal(0),
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    logger.info(f"Created copy of outdated budget: {budget.id} as new budget: {new_budget.id}")

    return new_budget
