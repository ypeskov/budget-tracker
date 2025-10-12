from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.Currency import Currency
from app.models.Transaction import Transaction
from app.models.User import User

LABEL_MAX_LENGTH = 50


class RecurrenceFrequencyEnum(Enum):
    """Frequency of recurring transactions"""

    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'


class PlannedTransaction(Base):
    """
    Model for planned/future transactions.
    Supports both one-time and recurring planned transactions.
    """

    __tablename__ = 'planned_transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), index=True
    )
    currency_id: Mapped[int] = mapped_column(
        ForeignKey('currencies.id', ondelete='CASCADE'), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(default=Decimal(0), nullable=False)
    label: Mapped[str] = mapped_column(
        String(LABEL_MAX_LENGTH), index=True, nullable=True, default=''
    )
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    is_income: Mapped[bool] = mapped_column(default=False)

    # Planning-specific fields
    planned_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, nullable=False
    )

    # Recurrence configuration
    is_recurring: Mapped[bool] = mapped_column(default=False, nullable=False)
    recurrence_rule: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # recurrence_rule structure:
    # {
    #   "frequency": "daily" | "weekly" | "monthly" | "yearly",
    #   "interval": 1,  # every N days/weeks/months/years
    #   "end_date": "2025-12-31T00:00:00Z",  # optional, ISO format
    #   "count": 10,  # optional, number of occurrences (exclusive with end_date)
    #   "day_of_week": 1,  # optional, for weekly (0=Monday, 6=Sunday)
    #   "day_of_month": 15  # optional, for monthly
    # }

    # Execution tracking
    is_executed: Mapped[bool] = mapped_column(
        default=False, nullable=False, server_default='f'
    )
    executed_transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey('transactions.id', ondelete='SET NULL'), index=True, nullable=True
    )
    execution_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Status flags
    is_active: Mapped[bool] = mapped_column(
        default=True, nullable=False, server_default='t'
    )
    is_deleted: Mapped[bool] = mapped_column(
        default=False, nullable=False, server_default='f'
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user: Mapped[User] = relationship(backref='planned_transactions')
    currency: Mapped[Currency] = relationship('Currency')
    executed_transaction: Mapped[Transaction | None] = relationship(
        'Transaction', foreign_keys='PlannedTransaction.executed_transaction_id'
    )

    def __repr__(self):  # pragma: no cover
        return (
            f'PlannedTransaction(id={self.id}, user_id={self.user_id}, '
            f'amount={self.amount}, label="{self.label}", '
            f'notes="{self.notes}", planned_date={self.planned_date}, is_income={self.is_income}, '
            f'is_recurring={self.is_recurring}, is_executed={self.is_executed}, '
            f'executed_transaction_id={self.executed_transaction_id}, is_active={self.is_active}, '
            f'is_deleted={self.is_deleted}, created_at={self.created_at}, updated_at={self.updated_at})'
        )
