from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    email = Column(String, unique=True, index=True, nullable=True)
    first_name = Column('firstName', String, unique=False, index=True, nullable=True)
    last_name = Column('lastName', String, unique=False, index=True, nullable=True)
    password_hash = Column('passwordHash', String, unique=False, index=True, nullable=True)
    is_active = Column('isActive', Boolean, unique=False, index=True, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
