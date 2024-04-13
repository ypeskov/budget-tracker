from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base


class ExchangeRateHistory(Base):
    __tablename__ = 'exchange_rates'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rates: Mapped[dict] = mapped_column(JSONB, nullable=True)
    datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True, server_default='f')
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)
