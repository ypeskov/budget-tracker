"""fix_planned_transactions_amount_precision

Revision ID: ed93d09cf19a
Revises: ce312ab0f469
Create Date: 2025-10-05 14:33:37.438040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed93d09cf19a'
down_revision = 'ce312ab0f469'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Change amount column to Numeric(15, 2) for proper precision
    op.alter_column('planned_transactions', 'amount',
                    type_=sa.Numeric(precision=15, scale=2),
                    existing_type=sa.Numeric(),
                    existing_nullable=False)


def downgrade() -> None:
    # Revert to unlimited Numeric
    op.alter_column('planned_transactions', 'amount',
                    type_=sa.Numeric(),
                    existing_type=sa.Numeric(precision=15, scale=2),
                    existing_nullable=False)
