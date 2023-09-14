from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.database import Base

SHORT_DESCRIPTION_MAX_LENGTH = 50


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), index=True)
    category_id = Column(Integer, ForeignKey('user_categories.id'), index=True)
    currency_id = Column(Integer, ForeignKey('currencies.id'), index=True)
    amount_in_currency = Column(Numeric)
    short_description = Column(String(SHORT_DESCRIPTION_MAX_LENGTH), index=True)
    long_description = Column(String)
    datetime = Column(DateTime(timezone=True), index=True)
    exchange_rate = Column(Numeric)

    account = relationship("Account")
    category = relationship("UserCategory")
    currency = relationship("Currency")

    is_deleted = Column(Boolean, default=False, nullable=True, server_default='f')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)