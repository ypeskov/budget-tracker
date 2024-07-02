"""add is_archived field to budgets table

Revision ID: 51533b59f1dd
Revises: 42a9b8a059f9
Create Date: 2024-07-02 22:33:16.210758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51533b59f1dd'
down_revision = '42a9b8a059f9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('budgets', sa.Column('is_archived', sa.Boolean(), server_default='f', nullable=False))
    op.alter_column('budgets', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('budgets', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    op.drop_column('budgets', 'is_archived')
    # ### end Alembic commands ###
