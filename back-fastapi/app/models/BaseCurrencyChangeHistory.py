from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.Currency import Currency
    from app.models.User import User


class BaseCurrencyChangeHistory(Base):
    __tablename__ = 'base_currency_change_history'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    base_currency_id: Mapped[int] = mapped_column(
        ForeignKey('currencies.id', ondelete='CASCADE')
    )
    change_date_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, default=func.now()
    )

    user: Mapped['User'] = relationship()
    base_currency: Mapped['Currency'] = relationship()

    is_deleted: Mapped[bool] = mapped_column(
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
