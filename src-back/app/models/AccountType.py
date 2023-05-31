from sqlalchemy import Column, String, Integer, DateTime, func, Boolean

from app.database import Base

ACCOUNT_TYPE_NAME_MAX_LENGTH = 100


class AccountType(Base):
    __tablename__ = 'account_types'

    id = Column(Integer, primary_key=True)

    type_name = Column(String(ACCOUNT_TYPE_NAME_MAX_LENGTH), index=True)
    is_credit = Column(Boolean, nullable=False, server_default='f')

    is_deleted = Column(Boolean, default=False, nullable=True, server_default='f')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
