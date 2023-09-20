from sqlalchemy import Column, String, Integer, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Currency(Base):
    __tablename__ = 'currencies'

    id = mapped_column(Integer, primary_key=True)
    code = mapped_column(String, index=True)
    name = mapped_column(String, index=True)

    is_deleted = mapped_column(Boolean, default=False, nullable=True, server_default='f')
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
