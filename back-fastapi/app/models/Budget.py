from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import String, DateTime, func, ForeignKey, Enum as SqlAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.User import User


class PeriodEnum(Enum):
    DAILY = 'day'
    WEEKLY = 'week'
    MONTHLY = 'month'
    YEARLY = 'year'
    CUSTOM = 'custom'


class Budget(Base):
    __tablename__ = 'budgets'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    target_amount: Mapped[Decimal] = mapped_column(default=0)
    collected_amount: Mapped[Decimal] = mapped_column(default=0)
    period: Mapped[PeriodEnum] = mapped_column(SqlAlchemyEnum(PeriodEnum), nullable=False)
    repeat: Mapped[bool] = mapped_column(default=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    included_categories: Mapped[str] = mapped_column(String(100), nullable=True)
    comment: Mapped[str] = mapped_column(nullable=True)

    user: Mapped[User] = relationship(backref="budgets", passive_deletes=True)

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=True, server_default='f')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)