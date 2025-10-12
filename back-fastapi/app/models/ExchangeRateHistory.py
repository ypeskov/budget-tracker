from datetime import date

from sqlalchemy import Boolean, Date, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import UniqueConstraint

from app.database import Base


class ExchangeRateHistory(Base):
    __tablename__ = 'exchange_rates'
    __table_args__ = (
        UniqueConstraint('service_name', 'actual_date', name='unique_service_date'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rates: Mapped[dict] = mapped_column(JSONB, nullable=True)
    actual_date: Mapped[date] = mapped_column(Date(), index=True)
    base_currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    service_name: Mapped[str] = mapped_column(String(50), nullable=False)

    is_deleted: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=True, server_default='f'
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
