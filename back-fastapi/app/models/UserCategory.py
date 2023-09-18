from datetime import datetime

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class UserCategory(Base):
    __tablename__ = 'user_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('user_categories.id'), nullable=True, index=True)
    is_income: Mapped[bool] = mapped_column(default=False, server_default='f')

    user = relationship("User", back_populates="categories")
    parent: Mapped['UserCategory'] = relationship("UserCategory")

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=True, server_default='f')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
