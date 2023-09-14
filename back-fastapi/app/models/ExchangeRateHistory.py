from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.database import Base


class ExchangeRateHistory(Base):
    __tablename__ = 'exchange_rates'

    id = Column(Integer, primary_key=True)
    from_currency_id = Column(Integer, ForeignKey('currencies.id'))
    to_currency_id = Column(Integer, ForeignKey('currencies.id'))
    rate = Column(Numeric)
    datetime = Column(DateTime(timezone=True), index=True)

    from_currency = relationship("Currency", foreign_keys=[from_currency_id])
    to_currency = relationship("Currency", foreign_keys=[to_currency_id])

    is_deleted = Column(Boolean, default=False, nullable=True, server_default='f')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
