from decimal import Decimal
from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base

from .AccountType import AccountType
from .User import User
from .Currency import Currency
from .Transaction import Transaction

ACCOUNT_NAME_MAX_LENGTH = 100


class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    account_type_id: Mapped[int] = mapped_column(ForeignKey('account_types.id'))
    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id'))
    balance: Mapped[Decimal] = mapped_column(default=0)
    name: Mapped[str] = mapped_column(String(ACCOUNT_NAME_MAX_LENGTH), index=True)
    opening_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    comment: Mapped[str] = mapped_column()
    is_hidden: Mapped[bool] = mapped_column(default=True)

    user: Mapped[User] = relationship(back_populates="accounts")
    account_type: Mapped[AccountType] = relationship()
    currency: Mapped[Currency] = relationship()
    transactions: Mapped[Transaction] = relationship(back_populates='account', foreign_keys='Transaction.account_id')
    target_transactions: Mapped[Transaction] = relationship(back_populates='target_account',
                                                            foreign_keys='[Transaction.target_account_id]')

    is_deleted = mapped_column(default=False, nullable=True, server_default='f')
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f'Account(id={self.id}, user_id={self.user_id}, account_type_id={self.account_type_id}) ' + \
            f'currency_id={self.currency_id}, balance={self.balance}, name="{self.name}", ' + \
            f'opening_date={self.opening_date}, comment="{self.comment}", is_hidden={self.is_hidden}, ' + \
            f'is_deleted={self.is_deleted}, created_at={self.created_at}, updated_at={self.updated_at}'
