from sqlalchemy import Column, String, Boolean, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from .Account import Account

from app.database import Base


DEFAULT_CURRENCY_CODE = 'USD'


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, server_default='t')
    base_currency_id = Column(Integer, ForeignKey('currencies.id'))

    base_currency = relationship("Currency")
    accounts = relationship("Account", order_by="Account.id", back_populates="user")
    categories = relationship("UserCategory", back_populates="user")

    is_deleted = Column(Boolean, default=False, nullable=True, server_default='f')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
