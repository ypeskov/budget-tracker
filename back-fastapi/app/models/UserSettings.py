from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database import Base
from app.models.User import User


class UserSettings(Base):
    __tablename__ = 'user_settings'

    id: Mapped[int] = mapped_column(primary_key=True)
    settings: Mapped[dict] = mapped_column(JSON, default=lambda: {})

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user: Mapped[User] = relationship(backref='settings')

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now(), onupdate=func.now(), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):  # pragma: no cover
        return f'UserSettings(id={self.id}, settings={self.settings}, user={self.user}, ' \
               f'created_at={self.created_at}, updated_at={self.updated_at})'
