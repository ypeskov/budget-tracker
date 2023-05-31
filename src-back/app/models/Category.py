from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

ACCOUNT_NAME_MAX_LENGTH = 100

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    parent_id = Column(Integer, ForeignKey('categories.id'))

    parent = relationship("Category")

    is_deleted = Column(Boolean, default=False, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)