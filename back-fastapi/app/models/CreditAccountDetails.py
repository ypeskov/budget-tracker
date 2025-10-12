from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.Account import Account

CR_ACCOUNT_NAME_MAX_LENGTH = 100


class CreditAccountDetails(Base):
    __tablename__ = 'credit_account_details'

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey('accounts.id', ondelete='CASCADE')
    )
    own_balance: Mapped[Decimal] = mapped_column()
    credit_balance: Mapped[Decimal] = mapped_column()

    account: Mapped['Account'] = relationship()

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
