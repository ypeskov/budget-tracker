from datetime import datetime

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class DefaultCategory(Base):
    __tablename__ = 'default_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('default_categories.id', ondelete='CASCADE'), nullable=True,
                                           default=None, server_default=None)
    is_income: Mapped[bool] = mapped_column(default=False, server_default='f')

    parent: Mapped['DefaultCategory'] = relationship(backref='children', remote_side='DefaultCategory.id')

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False, server_default='f')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now())
