from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.database import Base

CR_ACCOUNT_NAME_MAX_LENGTH = 100


class CreditAccountDetails(Base):
    __tablename__ = 'credit_account_details'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    own_balance = Column(Numeric)
    credit_balance = Column(Numeric)

    account = relationship("Account")

    is_deleted = Column(Boolean, default=False, nullable=True, server_default='f')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
