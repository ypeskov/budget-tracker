"""Updated migrations

Revision ID: aa6f55d2c0c3
Revises: 
Create Date: 2024-04-12 18:02:48.877056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa6f55d2c0c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type_name', sa.String(length=100), nullable=False),
    sa.Column('is_credit', sa.Boolean(), server_default='f', nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_account_types_type_name'), 'account_types', ['type_name'], unique=False)
    op.create_table('currencies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=3), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_currencies_code'), 'currencies', ['code'], unique=False)
    op.create_index(op.f('ix_currencies_name'), 'currencies', ['name'], unique=False)
    op.create_table('default_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('is_income', sa.Boolean(), server_default='f', nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['default_categories.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_default_categories_name'), 'default_categories', ['name'], unique=False)
    op.create_table('languages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.Column('is_active', sa.String(), server_default='t', nullable=False),
    sa.Column('base_currency_id', sa.Integer(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['base_currency_id'], ['currencies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('account_type_id', sa.Integer(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('initial_balance', sa.Numeric(), nullable=False),
    sa.Column('balance', sa.Numeric(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('opening_date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('is_hidden', sa.Boolean(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['account_type_id'], ['account_types.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_name'), 'accounts', ['name'], unique=False)
    op.create_index(op.f('ix_accounts_user_id'), 'accounts', ['user_id'], unique=False)
    op.create_table('user_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('is_income', sa.Boolean(), server_default='f', nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['user_categories.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_categories_name'), 'user_categories', ['name'], unique=False)
    op.create_index(op.f('ix_user_categories_parent_id'), 'user_categories', ['parent_id'], unique=False)
    op.create_index(op.f('ix_user_categories_user_id'), 'user_categories', ['user_id'], unique=False)
    op.create_table('user_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('settings', sa.JSON(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Numeric(), nullable=False),
    sa.Column('new_balance', sa.Numeric(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('label', sa.String(length=50), nullable=True),
    sa.Column('is_income', sa.Boolean(), nullable=False),
    sa.Column('is_transfer', sa.Boolean(), server_default='f', nullable=False),
    sa.Column('linked_transaction_id', sa.Integer(), nullable=True),
    sa.Column('base_currency_amount', sa.Numeric(), nullable=True),
    sa.Column('notes', sa.String(), nullable=True),
    sa.Column('date_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['category_id'], ['user_categories.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['linked_transaction_id'], ['transactions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_account_id'), 'transactions', ['account_id'], unique=False)
    op.create_index(op.f('ix_transactions_category_id'), 'transactions', ['category_id'], unique=False)
    op.create_index(op.f('ix_transactions_date_time'), 'transactions', ['date_time'], unique=False)
    op.create_index(op.f('ix_transactions_label'), 'transactions', ['label'], unique=False)
    op.create_index(op.f('ix_transactions_linked_transaction_id'), 'transactions', ['linked_transaction_id'], unique=False)
    op.create_index(op.f('ix_transactions_user_id'), 'transactions', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transactions_user_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_linked_transaction_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_label'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_date_time'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_category_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_account_id'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_table('user_settings')
    op.drop_index(op.f('ix_user_categories_user_id'), table_name='user_categories')
    op.drop_index(op.f('ix_user_categories_parent_id'), table_name='user_categories')
    op.drop_index(op.f('ix_user_categories_name'), table_name='user_categories')
    op.drop_table('user_categories')
    op.drop_index(op.f('ix_accounts_user_id'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_name'), table_name='accounts')
    op.drop_table('accounts')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('languages')
    op.drop_index(op.f('ix_default_categories_name'), table_name='default_categories')
    op.drop_table('default_categories')
    op.drop_index(op.f('ix_currencies_name'), table_name='currencies')
    op.drop_index(op.f('ix_currencies_code'), table_name='currencies')
    op.drop_table('currencies')
    op.drop_index(op.f('ix_account_types_type_name'), table_name='account_types')
    op.drop_table('account_types')
    # ### end Alembic commands ###