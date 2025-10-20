from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:  # pragma: no cover
    from app.models.TransactionTemplate import TransactionTemplate
    from app.models.User import User


class UserCategory(Base):
    __tablename__ = 'user_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    parent_id: Mapped[int] = mapped_column(
        ForeignKey('user_categories.id', ondelete='CASCADE'), nullable=True, index=True
    )
    is_income: Mapped[bool] = mapped_column(default=False, server_default='f')

    user: Mapped['User'] = relationship(back_populates="categories")
    parent: Mapped['UserCategory'] = relationship()
    templates: Mapped[list['TransactionTemplate']] = relationship(back_populates="category")

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=True, server_default='f')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):  # pragma: no cover
        return (
            f'UserCategory(id={self.id}, user_id={self.user_id}, name="{self.name}", parent_id={self.parent_id}, '
            + f'is_income={self.is_income}, is_deleted={self.is_deleted}, created_at={self.created_at}, '
            + f'updated_at={self.updated_at}'
        )
