from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta

from sqlalchemy import select, and_
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound

from app.logger_config import logger
from app.models.PlannedTransaction import PlannedTransaction
from app.models.Transaction import Transaction
from app.models.User import User
from app.schemas.planned_transaction_schema import (
    CreatePlannedTransactionSchema,
    UpdatePlannedTransactionSchema,
    PlannedTransactionOccurrenceSchema,
    RecurrenceFrequencyEnum,
)
from app.services.errors import AccessDenied


def create_planned_transaction(
    transaction_dto: CreatePlannedTransactionSchema,
    user_id: int,
    db: Session
) -> PlannedTransaction:
    """
    Create a new planned transaction.
    Amount is stored in user's base currency.

    Args:
        transaction_dto: Schema with planned transaction data
        user_id: ID of the user creating the transaction
        db: Database session

    Returns:
        Created PlannedTransaction instance
    """
    # Get user's base currency
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.base_currency_id:
        raise ValueError("User base currency not set")

    # Create planned transaction
    planned_transaction = PlannedTransaction(
        user_id=user_id,
        currency_id=user.base_currency_id,
        amount=transaction_dto.amount,
        label=transaction_dto.label,
        notes=transaction_dto.notes,
        is_income=transaction_dto.is_income,
        planned_date=transaction_dto.planned_date,
        is_recurring=transaction_dto.is_recurring,
        recurrence_rule=transaction_dto.recurrence_rule.model_dump(mode='json') if transaction_dto.recurrence_rule else None,
    )

    db.add(planned_transaction)
    db.commit()
    db.refresh(planned_transaction)

    logger.info(f"Created planned transaction {planned_transaction.id} for user {user_id}")

    return planned_transaction


def get_planned_transactions(
    user_id: int,
    db: Session,
    filters: dict | None = None
) -> list[PlannedTransaction]:
    """
    Get planned transactions for a user with optional filters.

    Args:
        user_id: ID of the user
        db: Database session
        filters: Optional dict with filters:
            - from_date: datetime
            - to_date: datetime
            - is_recurring: bool
            - is_executed: bool
            - is_active: bool
            - include_inactive: bool

    Returns:
        List of PlannedTransaction instances
    """
    stmt = (
        select(PlannedTransaction)
        .options(joinedload(PlannedTransaction.currency))
        .filter(
            PlannedTransaction.user_id == user_id,
            PlannedTransaction.is_deleted == False  # noqa: E712
        )
        .order_by(PlannedTransaction.planned_date.asc())
    )

    if filters:

        if 'from_date' in filters:
            stmt = stmt.filter(PlannedTransaction.planned_date >= filters['from_date'])

        if 'to_date' in filters:
            stmt = stmt.filter(PlannedTransaction.planned_date <= filters['to_date'])

        if 'is_recurring' in filters:
            stmt = stmt.filter(PlannedTransaction.is_recurring == filters['is_recurring'])

        if 'is_executed' in filters:
            stmt = stmt.filter(PlannedTransaction.is_executed == filters['is_executed'])

        if 'is_active' in filters:
            stmt = stmt.filter(PlannedTransaction.is_active == filters['is_active'])
        elif not filters.get('include_inactive', False):
            # By default, exclude inactive unless explicitly requested
            stmt = stmt.filter(PlannedTransaction.is_active == True)  # noqa: E712

    result = db.execute(stmt)
    return list(result.scalars().all())


def get_planned_transaction_by_id(
    planned_transaction_id: int,
    user_id: int,
    db: Session
) -> PlannedTransaction:
    """
    Get a specific planned transaction by ID.

    Args:
        planned_transaction_id: ID of the planned transaction
        user_id: ID of the user
        db: Database session

    Returns:
        PlannedTransaction instance

    Raises:
        AccessDenied: If transaction doesn't belong to user
        NoResultFound: If transaction not found
    """
    stmt = (
        select(PlannedTransaction)
        .options(joinedload(PlannedTransaction.currency))
        .filter(
            PlannedTransaction.id == planned_transaction_id,
            PlannedTransaction.is_deleted == False  # noqa: E712
        )
    )

    result = db.execute(stmt)
    planned_transaction = result.scalar_one_or_none()

    if not planned_transaction:
        raise NoResultFound(f"Planned transaction {planned_transaction_id} not found")

    if planned_transaction.user_id != user_id:
        raise AccessDenied(f"Access denied to planned transaction {planned_transaction_id}")

    return planned_transaction


def update_planned_transaction(
    planned_transaction_id: int,
    transaction_dto: UpdatePlannedTransactionSchema,
    user_id: int,
    db: Session
) -> PlannedTransaction:
    """
    Update a planned transaction.

    Args:
        planned_transaction_id: ID of the planned transaction to update
        transaction_dto: Schema with updated data
        user_id: ID of the user
        db: Database session

    Returns:
        Updated PlannedTransaction instance

    Raises:
        AccessDenied: If transaction doesn't belong to user
        NoResultFound: If transaction not found
    """
    planned_transaction = get_planned_transaction_by_id(planned_transaction_id, user_id, db)

    # Update fields
    planned_transaction.amount = transaction_dto.amount
    planned_transaction.label = transaction_dto.label
    planned_transaction.notes = transaction_dto.notes
    planned_transaction.is_income = transaction_dto.is_income
    planned_transaction.planned_date = transaction_dto.planned_date
    planned_transaction.is_recurring = transaction_dto.is_recurring
    planned_transaction.recurrence_rule = transaction_dto.recurrence_rule.model_dump(mode='json') if transaction_dto.recurrence_rule else None

    if transaction_dto.is_active is not None:
        planned_transaction.is_active = transaction_dto.is_active

    db.commit()
    db.refresh(planned_transaction)

    logger.info(f"Updated planned transaction {planned_transaction_id} for user {user_id}")

    return planned_transaction


def delete_planned_transaction(
    planned_transaction_id: int,
    user_id: int,
    db: Session
) -> None:
    """
    Soft delete a planned transaction.

    Args:
        planned_transaction_id: ID of the planned transaction to delete
        user_id: ID of the user
        db: Database session

    Raises:
        AccessDenied: If transaction doesn't belong to user
        NoResultFound: If transaction not found
    """
    planned_transaction = get_planned_transaction_by_id(planned_transaction_id, user_id, db)

    planned_transaction.is_deleted = True
    planned_transaction.is_active = False

    db.commit()

    logger.info(f"Deleted planned transaction {planned_transaction_id} for user {user_id}")


def generate_occurrences(
    planned_transaction: PlannedTransaction,
    start_date: datetime,
    end_date: datetime
) -> list[PlannedTransactionOccurrenceSchema]:
    """
    Generate occurrences of a recurring planned transaction within a date range.

    Args:
        planned_transaction: PlannedTransaction instance
        start_date: Start of the date range
        end_date: End of the date range

    Returns:
        List of PlannedTransactionOccurrenceSchema instances
    """
    # Ensure start_date and end_date are timezone-aware
    if start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=timezone.utc)
    if end_date.tzinfo is None:
        end_date = end_date.replace(tzinfo=timezone.utc)

    # Ensure planned_date is timezone-aware
    planned_date = planned_transaction.planned_date
    if planned_date.tzinfo is None:
        planned_date = planned_date.replace(tzinfo=timezone.utc)

    if not planned_transaction.is_recurring or not planned_transaction.recurrence_rule:
        # For non-recurring transactions, return single occurrence if within range
        if start_date <= planned_date <= end_date:
            return [PlannedTransactionOccurrenceSchema(
                planned_transaction_id=planned_transaction.id,
                occurrence_date=planned_date,
                amount=planned_transaction.amount,
                is_income=planned_transaction.is_income,
                label=planned_transaction.label,
                is_active=planned_transaction.is_active
            )]
        return []

    rule = planned_transaction.recurrence_rule
    frequency = rule['frequency']
    interval = rule.get('interval', 1)
    rule_end_date = None
    if rule.get('end_date'):
        if isinstance(rule['end_date'], str):
            rule_end_date = datetime.fromisoformat(rule['end_date'].replace('Z', '+00:00'))
        else:
            rule_end_date = rule['end_date']
        # Ensure rule_end_date is timezone-aware
        if rule_end_date.tzinfo is None:
            rule_end_date = rule_end_date.replace(tzinfo=timezone.utc)
    count = rule.get('count')

    occurrences = []
    current_date = planned_date

    # Determine the effective end date
    effective_end_date = end_date
    if rule_end_date and rule_end_date < effective_end_date:
        effective_end_date = rule_end_date

    occurrence_count = 0
    max_iterations = 1000  # Safety limit to prevent infinite loops

    while current_date <= effective_end_date and occurrence_count < max_iterations:
        # Check if we've reached the count limit
        if count is not None and occurrence_count >= count:
            break

        # Add occurrence if within range
        if start_date <= current_date <= end_date:
            occurrences.append(PlannedTransactionOccurrenceSchema(
                planned_transaction_id=planned_transaction.id,
                occurrence_date=current_date,
                amount=planned_transaction.amount,
                is_income=planned_transaction.is_income,
                label=planned_transaction.label,
                is_active=planned_transaction.is_active
            ))

        # Always increment occurrence count for recurring transactions
        occurrence_count += 1

        # Calculate next occurrence date
        if frequency == RecurrenceFrequencyEnum.DAILY.value:
            current_date += timedelta(days=interval)
        elif frequency == RecurrenceFrequencyEnum.WEEKLY.value:
            current_date += timedelta(weeks=interval)
        elif frequency == RecurrenceFrequencyEnum.MONTHLY.value:
            current_date += relativedelta(months=interval)
            # Handle day_of_month if specified
            if 'day_of_month' in rule and rule['day_of_month'] is not None:
                day_of_month = min(rule['day_of_month'], 28)  # Ensure valid day
                current_date = current_date.replace(day=day_of_month)
        elif frequency == RecurrenceFrequencyEnum.YEARLY.value:
            current_date += relativedelta(years=interval)
        else:
            break  # Unknown frequency

    return occurrences


def get_upcoming_occurrences(
    user_id: int,
    end_date: datetime,
    include_inactive: bool,
    db: Session
) -> list[PlannedTransactionOccurrenceSchema]:
    """
    Get all upcoming transaction occurrences for a user within the time range.

    Args:
        user_id: ID of the user
        end_date: End date for occurrences
        include_inactive: Include inactive planned transactions
        db: Database session

    Returns:
        List of PlannedTransactionOccurrenceSchema sorted by occurrence_date
    """
    # Get all non-deleted, non-executed planned transactions
    filters = {
        'is_executed': False,
        'include_inactive': include_inactive,
    }

    if not include_inactive:
        filters['is_active'] = True

    planned_transactions = get_planned_transactions(user_id, db, filters)

    all_occurrences = []

    # Generate occurrences for each planned transaction
    for pt in planned_transactions:
        # For non-executed transactions, include past occurrences to show overdue items
        # Look back up to 365 days to catch overdue transactions
        lookback_start = datetime.now(timezone.utc) - timedelta(days=365)

        # If planned_date is in the past but within lookback window, start from there
        # Otherwise start from now
        if pt.planned_date < datetime.now(timezone.utc) and pt.planned_date > lookback_start:
            start_date = pt.planned_date
        else:
            start_date = datetime.now(timezone.utc)

        occurrences = generate_occurrences(
            planned_transaction=pt,
            start_date=start_date,
            end_date=end_date
        )
        all_occurrences.extend(occurrences)

    # Sort by occurrence date
    all_occurrences.sort(key=lambda x: x.occurrence_date)

    return all_occurrences


