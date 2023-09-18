"""updated DefaultCategory and UserCategory to annotated

Revision ID: e146c8b916b1
Revises: 444d952babdf
Create Date: 2023-09-18 10:43:54.522822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e146c8b916b1'
down_revision = '444d952babdf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('default_categories', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('default_categories', 'is_income',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('default_categories', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    op.alter_column('user_categories', 'is_income',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_categories', 'is_income',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('default_categories', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    op.alter_column('default_categories', 'is_income',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('default_categories', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
