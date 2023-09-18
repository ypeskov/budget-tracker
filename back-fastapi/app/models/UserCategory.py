from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base

if TYPE_CHECKING:
    from app.models.User import User


class UserCategory(Base):
    __tablename__ = 'user_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('user_categories.id'), nullable=True, index=True)
    is_income: Mapped[bool] = mapped_column(default=False, server_default='f')

    user: Mapped['User'] = relationship(back_populates="categories")
    parent: Mapped['UserCategory'] = relationship()

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=True, server_default='f')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'UserCategory(id={self.id}, user_id={self.user_id}, name="{self.name}", parent_id={self.parent_id}, ' +\
            f'is_income={self.is_income}, is_deleted={self.is_deleted}, created_at={self.created_at}, ' + \
            f'updated_at={self.updated_at}'
