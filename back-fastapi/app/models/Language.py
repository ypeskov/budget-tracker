from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base

LANGUAGE_NAME_MAX_LENGTH = 50


class Language(Base):
    __tablename__ = 'languages'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[str] = mapped_column(String(LANGUAGE_NAME_MAX_LENGTH), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=True, server_default='f')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):  # pragma: no cover
        return f'Language(id={self.id}, name="{self.name}", code="{self.code}", is_deleted={self.is_deleted}, ' + \
            f'created_at={self.created_at}, updated_at={self.updated_at})'
