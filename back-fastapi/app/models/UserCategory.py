from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class UserCategory(Base):
    __tablename__ = 'user_categories'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey('user_categories.id'), nullable=True, index=True)
    is_income = Column(Boolean, default='f', server_default='f')

    user = relationship("User", back_populates="categories")
    parent = relationship("UserCategory")

    is_deleted = Column(Boolean, default=False, nullable=True, server_default='f')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
