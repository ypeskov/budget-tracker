"""change is_active to bool

Revision ID: 43861b1c72d0
Revises: 881a2b1a20be
Create Date: 2024-06-05 13:54:55.584170

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '43861b1c72d0'
down_revision = '881a2b1a20be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("UPDATE users SET is_active = 't' WHERE is_active = 'True'")
    op.execute("UPDATE users SET is_active = 'f' WHERE is_active = 'False'")

    op.execute("ALTER TABLE users ALTER COLUMN is_active DROP DEFAULT")

    op.alter_column('users', 'is_active',
                    existing_type=sa.VARCHAR(),
                    type_=sa.Boolean(),
                    existing_nullable=False,
                    postgresql_using="is_active::BOOLEAN")

    op.execute("ALTER TABLE users ALTER COLUMN is_active SET DEFAULT true")


def downgrade() -> None:
    op.execute("ALTER TABLE users ALTER COLUMN is_active DROP DEFAULT")

    op.alter_column('users', 'is_active',
                    existing_type=sa.Boolean(),
                    type_=sa.VARCHAR(),
                    existing_nullable=False,
                    postgresql_using="is_active::VARCHAR")

    op.execute("UPDATE users SET is_active = 'True' WHERE is_active = 't'")
    op.execute("UPDATE users SET is_active = 'False' WHERE is_active = 'f'")

    op.execute("ALTER TABLE users ALTER COLUMN is_active SET DEFAULT 't'::character varying")
