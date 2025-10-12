from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Currency(Base):
    __tablename__ = 'currencies'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(3), index=True)
    name: Mapped[str] = mapped_column(String, index=True)

    is_deleted: Mapped[bool] = mapped_column(
        default=False, nullable=True, server_default='f'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):  # pragma: no cover
        return f'<Currency id: {self.id}, code: {self.code}, name: {self.name}>'
