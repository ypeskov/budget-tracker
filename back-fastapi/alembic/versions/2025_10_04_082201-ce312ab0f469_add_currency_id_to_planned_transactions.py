"""add_currency_id_to_planned_transactions

Revision ID: ce312ab0f469
Revises: ac5b07035022
Create Date: 2025-10-04 08:22:01.746548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce312ab0f469'
down_revision = 'ac5b07035022'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add currency_id column (nullable first)
    op.add_column('planned_transactions', sa.Column('currency_id', sa.Integer(), nullable=True))

    # Set currency_id to user's base currency for existing records
    op.execute("""
        UPDATE planned_transactions pt
        SET currency_id = u.base_currency_id
        FROM users u
        WHERE pt.user_id = u.id
    """)

    # Make currency_id NOT NULL
    op.alter_column('planned_transactions', 'currency_id', nullable=False)

    # Add foreign key constraint
    op.create_foreign_key(
        'planned_transactions_currency_id_fkey',
        'planned_transactions',
        'currencies',
        ['currency_id'],
        ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    # Drop foreign key constraint
    op.drop_constraint('planned_transactions_currency_id_fkey', 'planned_transactions', type_='foreignkey')

    # Drop column
    op.drop_column('planned_transactions', 'currency_id')
