from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base
from app.models.User import User
from app.models.UserCategory import UserCategory

if TYPE_CHECKING:  # pragma: no cover
    from app.models.Account import Account

LABEL_MAX_LENGTH = 50


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id', ondelete='CASCADE'), index=True)
    amount: Mapped[Decimal] = mapped_column(default=Decimal(0), nullable=False)
    new_balance: Mapped[Decimal] = mapped_column(nullable=True, )
    category_id: Mapped[int | None] = mapped_column(ForeignKey('user_categories.id', ondelete='CASCADE'),
                                                    index=True, nullable=True)
    label: Mapped[str] = mapped_column(String(LABEL_MAX_LENGTH), index=True, nullable=True, default='')
    is_income: Mapped[bool] = mapped_column(default=False)
    is_transfer: Mapped[bool] = mapped_column(nullable=False, default=False, server_default='f')
    linked_transaction_id: Mapped[int | None] = mapped_column(ForeignKey('transactions.id', ondelete='CASCADE'),
                                                              index=True, nullable=True)
    base_currency_amount: Mapped[Decimal] = mapped_column(nullable=True)
    notes: Mapped[str] = mapped_column(nullable=True)
    date_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True, nullable=True)

    user: Mapped[User] = relationship(backref='transactions')
    account: Mapped['Account'] = relationship('Account', foreign_keys="Transaction.account_id")
    category: Mapped[UserCategory] = relationship()
    linked_transaction: Mapped['Transaction'] = relationship('Transaction',
                                                             foreign_keys='Transaction.linked_transaction_id',
                                                             remote_side='Transaction.id')

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=True, server_default='f')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(),
                                                 nullable=False)

    def __repr__(self):  # pragma: no cover
        return f'Transaction(id={self.id}, user_id={self.user_id}, account_id={self.account_id}, ' + \
            f'category_id={self.category_id}, amount={self.amount}, ' + \
            f'label="{self.label}", notes="{self.notes}", date_time={self.date_time}, ' + \
            f'is_transfer={self.is_transfer}, is_income = {self.is_income}, ' + \
            f'linked_transaction_id={self.linked_transaction_id}, ' + \
            f'is_deleted = {self.is_deleted}, created_at = {self.created_at}, updated_at = {self.updated_at})'


