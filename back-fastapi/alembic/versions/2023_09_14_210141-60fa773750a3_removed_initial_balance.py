"""removed initial balance

Revision ID: 60fa773750a3
Revises: 2971634b2f1a
Create Date: 2023-09-14 21:01:41.266549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60fa773750a3'
down_revision = '2971634b2f1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'opening_exchange_rate')
    op.drop_column('accounts', 'initial_balance')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('initial_balance', sa.NUMERIC(), autoincrement=False, nullable=True, comment='balance at the moment of account opening'))
    op.add_column('accounts', sa.Column('opening_exchange_rate', sa.NUMERIC(), autoincrement=False, nullable=True, comment='Account currency to base currency'))
    # ### end Alembic commands ###
