from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

ACCOUNT_TYPE_NAME_MAX_LENGTH = 100


class AccountType(Base):
    __tablename__ = 'account_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str] = mapped_column(String(ACCOUNT_TYPE_NAME_MAX_LENGTH), index=True)
    is_credit: Mapped[bool] = mapped_column(nullable=False, server_default='f')

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=True, server_default='f')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
