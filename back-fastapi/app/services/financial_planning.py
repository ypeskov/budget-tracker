from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.logger_config import logger
from app.models.Account import Account
from app.models.PlannedTransaction import PlannedTransaction
from app.models.User import User
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
    user = (
        db.query(User)
        .options(joinedload(User.base_currency))
        .filter(User.id == user_id)
        .first()
    )
    if not user or not user.base_currency:
        raise ValueError("User base currency not set")

    base_currency_code = user.base_currency.code

    # Get accounts
    accounts_query = (
        select(Account)
        .options(joinedload(Account.currency))
        .filter(
            Account.user_id == user_id,
            Account.is_deleted == False,  # noqa: E712
        )
    )

    if request.account_ids:
        accounts_query = accounts_query.filter(Account.id.in_(request.account_ids))
    else:
        # If no specific accounts requested, only include accounts shown in reports
        accounts_query = accounts_query.filter(Account.show_in_reports == True)  # noqa: E712

    accounts = list(db.execute(accounts_query).scalars().all())

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
            request.target_date.date()
            if hasattr(request.target_date, 'date')
            else request.target_date,
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
    total_projected_balance = (
        total_current_balance + total_planned_income - total_planned_expenses
    )

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
    user = (
        db.query(User)
        .options(joinedload(User.base_currency))
        .filter(User.id == user_id)
        .first()
    )
    if not user or not user.base_currency:
        raise ValueError("User base currency not set")

    base_currency_code = user.base_currency.code

    # Get accounts
    accounts_query = (
        select(Account)
        .options(joinedload(Account.currency))
        .filter(
            Account.user_id == user_id,
            Account.is_deleted == False,  # noqa: E712
        )
    )

    if request.account_ids:
        accounts_query = accounts_query.filter(Account.id.in_(request.account_ids))
    else:
        # If no specific accounts requested, only include accounts shown in reports
        accounts_query = accounts_query.filter(Account.show_in_reports == True)  # noqa: E712

    accounts = list(db.execute(accounts_query).scalars().all())

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
    current_date = request.start_date

    # Determine step size based on period
    if request.period == 'daily':
        step = timedelta(days=1)
    elif request.period == 'weekly':
        step = timedelta(weeks=1)
    elif request.period == 'monthly':
        step = timedelta(days=30)  # Approximate
    else:
        step = timedelta(days=1)

    # Calculate initial balance
    initial_balance = sum(
        calc_amount(
            account.balance,
            account.currency.code,
            current_date.date() if hasattr(current_date, 'date') else current_date,
            base_currency_code,
            db,
        )
        for account in accounts
    )

    running_balance = initial_balance

    while current_date <= request.end_date:
        # Calculate income and expenses for this period
        period_end = min(current_date + step, request.end_date)
        period_income = Decimal(0)
        period_expenses = Decimal(0)

        for planned_tx in planned_transactions:
            occurrences = generate_occurrences(
                planned_transaction=planned_tx,
                start_date=current_date,
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
                date=current_date,
                balance=running_balance,
                income=period_income,
                expenses=period_expenses,
            )
        )

        current_date = period_end
        if current_date == request.end_date:
            break

    return BalanceProjectionResponseSchema(
        start_date=request.start_date,
        end_date=request.end_date,
        period=request.period,
        base_currency_code=base_currency_code,
        projection_points=projection_points,
    )
