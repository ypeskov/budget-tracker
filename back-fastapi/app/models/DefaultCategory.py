from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.database import Base


class DefaultCategory(Base):
    __tablename__ = 'default_categories'

    id = Column(Integer, primary_key=True)

    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey('default_categories.id'))
    is_income = Column(Boolean, default=False, server_default='f')

    parent = relationship("DefaultCategory", backref=backref("children"), remote_side=[id])

    is_deleted = Column(Boolean, default=False, nullable=True, server_default='f')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
