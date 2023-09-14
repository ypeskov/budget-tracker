from sqlalchemy import Column, Integer, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class BaseCurrencyChangeHistory(Base):
    __tablename__ = 'base_currency_change_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    base_currency_id = Column(Integer, ForeignKey('currencies.id'))
    change_date_time = Column(DateTime(timezone=True), index=True, default=func.now())

    user = relationship("User")
    base_currency = relationship("Currency")

    is_deleted = Column(Boolean, default=False, nullable=True, server_default='f')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
