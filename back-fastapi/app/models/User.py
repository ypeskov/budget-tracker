from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base

if TYPE_CHECKING:  # pragma: no cover
    from app.models.UserCategory import UserCategory
    from app.models.Account import Account
    from app.models.Transaction import Transaction
    from app.models.Currency import Currency

DEFAULT_CURRENCY_CODE = 'USD'


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(index=True, nullable=True)
    last_name: Mapped[str] = mapped_column(index=True, nullable=True)
    password_hash: Mapped[str] = mapped_column()
    is_active: Mapped[str] = mapped_column(server_default='t', default=True)
    base_currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id', ondelete='CASCADE'))

    base_currency: Mapped['Currency'] = relationship()
    accounts: Mapped[list['Account']] = relationship('Account', order_by="Account.id", back_populates="user",
                                                     passive_deletes=True)
    categories: Mapped[list['UserCategory']] = relationship(back_populates="user", passive_deletes=True)
    transactions: Mapped[list['Transaction']] = relationship(back_populates='user', passive_deletes=True)

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False, server_default='f')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)
