from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base
from app.models.User import User

LABEL_MAX_LENGTH = 255

class TransactionTemplate(Base):
    __tablename__ = 'transaction_templates'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    label: Mapped[str] = mapped_column(String(LABEL_MAX_LENGTH), index=True, nullable=True, default='')
    category_id: Mapped[int | None] = mapped_column(ForeignKey('user_categories.id', ondelete='CASCADE'), index=True, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='transaction_templates')
    
    def __repr__(self):
        return (f'TransactionTemplate(id={self.id}, user_id={self.user_id}, label={self.label}, category_id={self.category_id}, '
            f'created_at={self.created_at}, updated_at={self.updated_at})')