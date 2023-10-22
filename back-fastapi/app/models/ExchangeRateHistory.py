from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Integer, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


if TYPE_CHECKING:
    from app.models.Currency import Currency


class ExchangeRateHistory(Base):
    __tablename__ = 'exchange_rates'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id', ondelete='CASCADE'))
    to_currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id', ondelete='CASCADE'))
    rate: Mapped[Decimal] = mapped_column()
    datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    from_currency: Mapped['Currency'] = relationship(foreign_keys=[from_currency_id])
    to_currency: Mapped['Currency'] = relationship(foreign_keys=[to_currency_id])

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True, server_default='f')
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)
