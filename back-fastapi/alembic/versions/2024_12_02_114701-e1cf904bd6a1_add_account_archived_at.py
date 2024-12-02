"""add Account.archived_at

Revision ID: e1cf904bd6a1
Revises: 36625efa3c6f
Create Date: 2024-12-02 11:47:01.488994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1cf904bd6a1'
down_revision = '36625efa3c6f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('archived_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'archived_at')
    # ### end Alembic commands ###
