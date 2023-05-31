from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.database import Base

ACCOUNT_NAME_MAX_LENGTH = 100

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    account_type_id = Column(Integer, ForeignKey('account_types.id'))
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    balance = Column(Numeric)
    name = Column(String(ACCOUNT_NAME_MAX_LENGTH))

    user = relationship("User", back_populates="accounts")
    account_type = relationship("AccountType")
    currency = relationship("Currency")

    is_deleted = Column(Boolean, default=False, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)