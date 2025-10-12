from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.AccountType import AccountType
from app.models.Currency import Currency
from app.models.User import User

if TYPE_CHECKING:  # pragma: no cover
    from .Transaction import Transaction

ACCOUNT_NAME_MAX_LENGTH = 100


class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), index=True
    )
    account_type_id: Mapped[int] = mapped_column(
        ForeignKey('account_types.id', ondelete='CASCADE')
    )
    currency_id: Mapped[int] = mapped_column(
        ForeignKey('currencies.id', ondelete='CASCADE')
    )
    initial_balance: Mapped[Decimal] = mapped_column(default=0)
    balance: Mapped[Decimal] = mapped_column(default=0)
    credit_limit: Mapped[Decimal] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(String(ACCOUNT_NAME_MAX_LENGTH), index=True)
    opening_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    comment: Mapped[str] = mapped_column(nullable=True)
    is_hidden: Mapped[bool] = mapped_column(default=False)
    show_in_reports: Mapped[bool] = mapped_column(default=True, nullable=True)

    user: Mapped[User] = relationship(backref="accounts", passive_deletes=True)
    account_type: Mapped[AccountType] = relationship()
    currency: Mapped[Currency] = relationship()
    transactions: Mapped['Transaction'] = relationship(
        back_populates='account', foreign_keys='Transaction.account_id'
    )

    archived_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    is_deleted: Mapped[bool] = mapped_column(
        default=False, nullable=True, server_default='f'
    )
    is_archived: Mapped[bool] = mapped_column(
        default=False, nullable=True, server_default='f'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):  # pragma: no cover
        return (
            f'Account(id={self.id}, user_id={self.user_id}, account_type_id={self.account_type_id} '
            + f'currency_id={self.currency_id}, initial_balance={self.initial_balance} balance={self.balance}, name="{self.name}", '
            + f'opening_date={self.opening_date}, comment="{self.comment}", is_hidden={self.is_hidden}, '
            + f'is_deleted={self.is_deleted}, created_at={self.created_at}, updated_at={self.updated_at})'
        )
