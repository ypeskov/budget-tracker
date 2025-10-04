"""remove_account_and_category_from_planned_transactions

Revision ID: ac5b07035022
Revises: ba5a10f71c14
Create Date: 2025-10-04 07:33:53.941877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac5b07035022'
down_revision = 'ba5a10f71c14'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop foreign key constraints first
    op.drop_constraint('planned_transactions_account_id_fkey', 'planned_transactions', type_='foreignkey')
    op.drop_constraint('planned_transactions_category_id_fkey', 'planned_transactions', type_='foreignkey')

    # Drop columns
    op.drop_column('planned_transactions', 'account_id')
    op.drop_column('planned_transactions', 'category_id')


def downgrade() -> None:
    # Add columns back
    op.add_column('planned_transactions', sa.Column('account_id', sa.INTEGER(), nullable=True))
    op.add_column('planned_transactions', sa.Column('category_id', sa.INTEGER(), nullable=True))

    # Recreate foreign key constraints
    op.create_foreign_key('planned_transactions_account_id_fkey', 'planned_transactions', 'accounts', ['account_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('planned_transactions_category_id_fkey', 'planned_transactions', 'user_categories', ['category_id'], ['id'], ondelete='CASCADE')
