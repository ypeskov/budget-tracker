from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import String, DateTime, func, ForeignKey, Enum as SqlAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.User import User
from app.models.Currency import Currency


class PeriodEnum(Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'
    CUSTOM = 'custom'


class Budget(Base):
    __tablename__ = 'budgets'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id', ondelete='CASCADE'), index=True)
    target_amount: Mapped[Decimal] = mapped_column(default=0)
    collected_amount: Mapped[Decimal] = mapped_column(default=0)
    period: Mapped[PeriodEnum] = mapped_column(SqlAlchemyEnum(PeriodEnum), nullable=False)
    repeat: Mapped[bool] = mapped_column(default=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    included_categories: Mapped[str] = mapped_column(String(100), nullable=True)
    comment: Mapped[str] = mapped_column(nullable=True)

    user: Mapped[User] = relationship(backref="budgets", passive_deletes=True)
    currency: Mapped[Currency] = relationship(backref="budgets", passive_deletes=True)

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False, server_default='f')
    is_archived: Mapped[bool] = mapped_column(default=False, nullable=False, server_default='f')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    def __repr__(self):
        return (f'Budget(id={self.id}, user_id={self.user_id}, name={self.name}, target_amount={self.target_amount}, '
                f'collected_amount={self.collected_amount}, period={self.period}, repeat={self.repeat}, '
                f'start_date={self.start_date}, end_date={self.end_date}, included_categories={self.included_categories}, '
                f'comment={self.comment}, is_deleted={self.is_deleted}, is_archived={self.is_archived})')
