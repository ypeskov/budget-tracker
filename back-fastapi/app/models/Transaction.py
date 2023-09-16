from decimal import Decimal
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base
from app.models.Currency import Currency
from app.models.User import User
from app.models.UserCategory import UserCategory


if TYPE_CHECKING:
    from app.models.Account import Account

LABEL_MAX_LENGTH = 50


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'), index=True)
    target_account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id'), index=True, nullable=True, default=None)
    category_id: Mapped[int] = mapped_column(ForeignKey('user_categories.id'), index=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id'), index=True)
    amount: Mapped[Decimal] = mapped_column()
    label: Mapped[str] = mapped_column(String(LABEL_MAX_LENGTH), index=True)
    notes: Mapped[str] = mapped_column()
    datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    exchange_rate: Mapped[Decimal] = mapped_column()
    is_transfer: Mapped[bool] = mapped_column(nullable=False)
    is_income: Mapped[bool] = mapped_column(default=False)

    user: Mapped[User] = relationship(back_populates='transactions')

    account: Mapped['Account'] = relationship('Account', foreign_keys="Transaction.account_id")

    target_account: Mapped['Account'] = relationship('Account', foreign_keys="Transaction.target_account_id")

    category: Mapped[UserCategory] = relationship()
    currency: Mapped[Currency] = relationship()

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=True, server_default='f')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(),
                                                 nullable=False)

    # def __str__(self):
    #     return f'Transaction: id:{self.id}, user:{self.user.id},' + \
    #         f' amount:{self.amount}{self.currency.code},' + \
    #         f' account:{self.account.name}'

    def __repr__(self):
        return f'Transaction(id={self.id}, user_id={self.user_id}), account_id={self.account_id}, ' + \
            f'target_account_id={self.target_account_id}, category_id={self.category_id}, amount={self.amount}, ' + \
            f'label={self.label}, notes={self.notes}, datetime={self.datetime}, exchange_rate={self.exchange_rate}, ' + \
            f'is_transfer={self.is_transfer}, is_income = {self.is_income}, is_deleted = {self.is_deleted}, ' + \
            f'created_at = {self.created_at}, updated_at = {self.updated_at}'
