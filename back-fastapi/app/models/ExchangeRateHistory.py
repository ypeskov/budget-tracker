from datetime import datetime,date

from sqlalchemy import Integer, DateTime, Date, func, Boolean, String
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base
from app.models.Currency import Currency


class ExchangeRateHistory(Base):
    __tablename__ = 'exchange_rates'
    __table_args__ = (UniqueConstraint('service_name', 'actual_date', name='unique_service_date'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rates: Mapped[dict] = mapped_column(JSONB, nullable=True)
    actual_date: Mapped[date] = mapped_column(Date(), index=True)
    base_currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    service_name: Mapped[str] = mapped_column(String(50), nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True, server_default='f')
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)
