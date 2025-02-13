from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base
from app.models import Currency
from app.models import UserCategory

if TYPE_CHECKING:
    from app.models.TransactionTemplate import TransactionTemplate

DEFAULT_CURRENCY_CODE = 'USD'


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(index=True, nullable=True)
    last_name: Mapped[str] = mapped_column(index=True, nullable=True)
    password_hash: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(server_default='t', default=True)
    base_currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id', ondelete='CASCADE'))

    base_currency: Mapped[Currency.Currency] = relationship()
    categories: Mapped[list[UserCategory.UserCategory]] = relationship(back_populates="user", passive_deletes=True)
    transaction_templates: Mapped[list['TransactionTemplate']] = relationship('TransactionTemplate', back_populates='user')
    
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False, server_default='f')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    def __repr__(self):  # pragma: no cover
        return f'User(id={self.id}, email="{self.email}", first_name="{self.first_name}", ' + \
            f'last_name="{self.last_name}", is_active={self.is_active}, base_currency_id={self.base_currency_id}, ' + \
            f'is_deleted={self.is_deleted}, created_at={self.created_at}, updated_at={self.updated_at})'
