from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.database import Base

ACCOUNT_NAME_MAX_LENGTH = 100


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    amount = Column(Numeric)
    description = Column(String)
    date_time = Column(DateTime)
    exchange_rate = Column(Numeric)

    account = relationship("Account")
    category = relationship("Category")
    currency = relationship("Currency")

    is_deleted = Column(Boolean, default=False, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)