from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.logger_config import logger
from app.models.PlannedTransaction import PlannedTransaction
from app.models.User import User
from app.services.accounts import get_user_accounts
from app.schemas.planned_transaction_schema import (
    AccountBalanceProjectionSchema,
    BalanceProjectionPointSchema,
    BalanceProjectionRequestSchema,
    BalanceProjectionResponseSchema,
    FutureBalanceRequestSchema,
    FutureBalanceResponseSchema,
)
from app.services.CurrencyProcessor import calc_amount
from app.services.planned_transactions import generate_occurrences


def calculate_future_balance(
    request: FutureBalanceRequestSchema, user_id: int, db: Session
) -> FutureBalanceResponseSchema:
    """
    Calculate projected balance on a future date considering planned transactions.

    Args:
        request: Request schema with target date and filters
        user_id: ID of the user
        db: Database session

    Returns:
        FutureBalanceResponseSchema with projected balances
    """
    # Get user's base currency
    user = db.query(User).options(joinedload(User.base_currency)).filter(User.id == user_id).first()
    if not user or not user.base_currency:
        raise ValueError("User base currency not set")

    base_currency_code = user.base_currency.code

    # Get accounts using the same service as accounts endpoint for consistency
    accounts = get_user_accounts(
        user_id=user_id,
        db=db,
        include_deleted=False,
        include_hidden=False,
        include_archived=False,
        archived_only=False,
    )

    # Filter by specific account IDs if provided
    if request.account_ids:
        accounts = [acc for acc in accounts if acc.id in request.account_ids]

    if not accounts:
        raise ValueError("No accounts found")

    # Get planned transactions
    planned_transactions_query = (
        select(PlannedTransaction)
        .options(joinedload(PlannedTransaction.currency))
        .filter(
            PlannedTransaction.user_id == user_id,
            PlannedTransaction.is_deleted == False,  # noqa: E712
            PlannedTransaction.is_executed == False,  # noqa: E712
            PlannedTransaction.planned_date <= request.target_date,
        )
    )

    if not request.include_inactive:
        planned_transactions_query = planned_transactions_query.filter(
            PlannedTransaction.is_active == True  # noqa: E712
        )

    if request.account_ids:
        planned_transactions_query = planned_transactions_query.filter(
            PlannedTransaction.account_id.in_(request.account_ids)
        )

    planned_transactions = list(db.execute(planned_transactions_query).scalars().all())

    # Calculate current balances
    account_projections = []
    total_current_balance = Decimal(0)
    total_planned_income = Decimal(0)
    total_planned_expenses = Decimal(0)
    total_income_count = 0
    total_expenses_count = 0

    for account in accounts:
        # Get current balance in base currency
        current_balance_base = calc_amount(
            account.balance,
            account.currency.code,
            datetime.now().date(),
            base_currency_code,
            db,
        )
        total_current_balance += current_balance_base

        # Calculate projected balance in account currency (without planned transactions)
        projected_balance_account_currency = account.balance

        # Convert projected balance to base currency
        projected_balance_base = calc_amount(
            projected_balance_account_currency,
            account.currency.code,
            request.target_date.date() if hasattr(request.target_date, 'date') else request.target_date,
            base_currency_code,
            db,
        )

        account_projections.append(
            AccountBalanceProjectionSchema(
                account_id=account.id,
                account_name=account.name,
                currency_code=account.currency.code,
                current_balance=account.balance,
                projected_balance=projected_balance_account_currency,
                total_planned_income=Decimal(0),
                total_planned_expenses=Decimal(0),
            )
        )

    # Calculate planned income and expenses from ALL planned transactions (not linked to specific accounts)
    for planned_tx in planned_transactions:
        # Generate occurrences for recurring transactions
        occurrences = generate_occurrences(
            planned_transaction=planned_tx,
            start_date=datetime.now(),
            end_date=request.target_date,
        )

        for occurrence in occurrences:
            # Convert amount from planned transaction currency to user's base currency
            amount_in_base_currency = calc_amount(
                occurrence.amount,
                planned_tx.currency.code,
                occurrence.occurrence_date.date()
                if hasattr(occurrence.occurrence_date, 'date')
                else occurrence.occurrence_date,
                base_currency_code,
                db,
            )

            if occurrence.is_income:
                total_planned_income += amount_in_base_currency
                total_income_count += 1
            else:
                total_planned_expenses += amount_in_base_currency
                total_expenses_count += 1

    # Calculate total projected balance
    total_projected_balance = total_current_balance + total_planned_income - total_planned_expenses

    return FutureBalanceResponseSchema(
        target_date=request.target_date,
        base_currency_code=base_currency_code,
        total_current_balance=total_current_balance,
        total_projected_balance=total_projected_balance,
        total_planned_income=total_planned_income,
        total_planned_expenses=total_planned_expenses,
        income_count=total_income_count,
        expenses_count=total_expenses_count,
        accounts=account_projections,
    )


def get_balance_projection(
    request: BalanceProjectionRequestSchema, user_id: int, db: Session
) -> BalanceProjectionResponseSchema:
    """
    Generate balance projection over a time period.

    Args:
        request: Request schema with date range and period
        user_id: ID of the user
        db: Database session

    Returns:
        BalanceProjectionResponseSchema with projection points
    """
    # Get user's base currency
    user = db.query(User).options(joinedload(User.base_currency)).filter(User.id == user_id).first()
    if not user or not user.base_currency:
        raise ValueError("User base currency not set")

    base_currency_code = user.base_currency.code

    # Get accounts using the same service as accounts endpoint for consistency
    accounts = get_user_accounts(
        user_id=user_id,
        db=db,
        include_deleted=False,
        include_hidden=False,
        include_archived=False,
        archived_only=False,
    )

    # Filter by specific account IDs if provided
    if request.account_ids:
        accounts = [acc for acc in accounts if acc.id in request.account_ids]

    if not accounts:
        raise ValueError("No accounts found")

    # Get all planned transactions in the range
    planned_transactions_query = (
        select(PlannedTransaction)
        .options(joinedload(PlannedTransaction.currency))
        .filter(
            PlannedTransaction.user_id == user_id,
            PlannedTransaction.is_deleted == False,  # noqa: E712
            PlannedTransaction.is_executed == False,  # noqa: E712
        )
    )

    if not request.include_inactive:
        planned_transactions_query = planned_transactions_query.filter(
            PlannedTransaction.is_active == True  # noqa: E712
        )

    planned_transactions = list(db.execute(planned_transactions_query).scalars().all())

    # Generate projection points based on period
    projection_points = []

    # Calculate initial balance
    initial_balance = Decimal(0)
    for account in accounts:
        balance_in_base = calc_amount(
            account.balance,
            account.currency.code,
            request.start_date.date() if hasattr(request.start_date, 'date') else request.start_date,
            base_currency_code,
            db,
        )
        initial_balance += balance_in_base

    running_balance = initial_balance

    # Helper function to get end of week (Sunday)
    def get_week_end(date):
        """Get the end of the week (Sunday) for the given date."""
        days_until_sunday = (6 - date.weekday()) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7
        return date + timedelta(days=days_until_sunday)

    # Helper function to get end of month
    def get_month_end(date):
        """Get the last day of the month for the given date."""
        if date.month == 12:
            next_month = date.replace(year=date.year + 1, month=1, day=1)
        else:
            next_month = date.replace(month=date.month + 1, day=1)
        return next_month - timedelta(days=1)

    # Generate date points based on period
    date_points = []
    current_date = request.start_date

    if request.period == 'daily':
        # For daily: just add each day
        while current_date <= request.end_date:
            date_points.append(current_date)
            current_date = current_date + timedelta(days=1)

    elif request.period == 'weekly':
        # First point is current date
        date_points.append(current_date)

        # Find next Monday after current date
        days_until_monday = (7 - current_date.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        next_monday = current_date + timedelta(days=days_until_monday)

        # Then add end of each week (Sunday)
        current_date = next_monday
        while current_date <= request.end_date:
            week_end = get_week_end(current_date)
            if week_end > request.end_date:
                week_end = request.end_date
            date_points.append(week_end)
            current_date = week_end + timedelta(days=1)

    elif request.period == 'monthly':
        # First point is current date
        date_points.append(current_date)

        # Find first day of next month
        if current_date.month == 12:
            next_month_start = current_date.replace(year=current_date.year + 1, month=1, day=1)
        else:
            next_month_start = current_date.replace(month=current_date.month + 1, day=1)

        # Then add end of each month
        current_date = next_month_start
        while current_date <= request.end_date:
            month_end = get_month_end(current_date)
            if month_end > request.end_date:
                month_end = request.end_date
            date_points.append(month_end)

            # Move to first day of next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1, day=1)

    # Now calculate balance for each date point
    for i, point_date in enumerate(date_points):
        # Calculate transactions from start (or previous point) to current point
        if i == 0:
            # For first point, start from the beginning of start_date (not current time)
            period_start = request.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            # For subsequent points, start from beginning of the day after previous point
            prev_point = date_points[i - 1]
            period_start = (prev_point + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        period_end = point_date
        # Ensure period_end includes the entire day (set to end of day)
        if hasattr(period_end, 'replace'):
            period_end = period_end.replace(hour=23, minute=59, second=59)

        period_income = Decimal(0)
        period_expenses = Decimal(0)

        for planned_tx in planned_transactions:
            occurrences = generate_occurrences(
                planned_transaction=planned_tx,
                start_date=period_start,
                end_date=period_end,
            )

            for occurrence in occurrences:
                # Convert amount from planned transaction currency to user's base currency
                amount_in_base_currency = calc_amount(
                    occurrence.amount,
                    planned_tx.currency.code,
                    occurrence.occurrence_date.date()
                    if hasattr(occurrence.occurrence_date, 'date')
                    else occurrence.occurrence_date,
                    base_currency_code,
                    db,
                )

                if occurrence.is_income:
                    period_income += amount_in_base_currency
                    running_balance += amount_in_base_currency
                else:
                    period_expenses += amount_in_base_currency
                    running_balance -= amount_in_base_currency

        projection_points.append(
            BalanceProjectionPointSchema(
                date=point_date,
                balance=running_balance,
                income=period_income,
                expenses=period_expenses,
            )
        )

    return BalanceProjectionResponseSchema(
        start_date=request.start_date,
        end_date=request.end_date,
        period=request.period,
        base_currency_code=base_currency_code,
        projection_points=projection_points,
    )
