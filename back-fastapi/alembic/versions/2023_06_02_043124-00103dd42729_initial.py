"""initial

Revision ID: 00103dd42729
Revises: 
Create Date: 2023-06-02 04:31:24.269160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00103dd42729'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type_name', sa.String(length=100), nullable=True),
    sa.Column('is_credit', sa.Boolean(), server_default='f', nullable=False),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_account_types_type_name'), 'account_types', ['type_name'], unique=False)
    op.create_table('currencies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_currencies_code'), 'currencies', ['code'], unique=False)
    op.create_index(op.f('ix_currencies_name'), 'currencies', ['name'], unique=False)
    op.create_table('default_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('is_income', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['default_categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_default_categories_name'), 'default_categories', ['name'], unique=False)
    op.create_table('exchange_rates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_currency_id', sa.Integer(), nullable=True),
    sa.Column('to_currency_id', sa.Integer(), nullable=True),
    sa.Column('rate', sa.Numeric(), nullable=True),
    sa.Column('datetime', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['from_currency_id'], ['currencies.id'], ),
    sa.ForeignKeyConstraint(['to_currency_id'], ['currencies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exchange_rates_datetime'), 'exchange_rates', ['datetime'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default='t', nullable=True),
    sa.Column('base_currency_id', sa.Integer(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['base_currency_id'], ['currencies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('account_type_id', sa.Integer(), nullable=True),
    sa.Column('currency_id', sa.Integer(), nullable=True),
    sa.Column('balance', sa.Numeric(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('opening_date', sa.Date(), nullable=True),
    sa.Column('initial_balance_in_currency', sa.Numeric(), nullable=True),
    sa.Column('opening_exchange_rate', sa.Numeric(), nullable=True, comment='Account currency to base currency'),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('show_in_transactions', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['account_type_id'], ['account_types.id'], ),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_name'), 'accounts', ['name'], unique=False)
    op.create_index(op.f('ix_accounts_user_id'), 'accounts', ['user_id'], unique=False)
    op.create_table('base_currency_change_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('base_currency_id', sa.Integer(), nullable=True),
    sa.Column('change_date_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['base_currency_id'], ['currencies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_base_currency_change_history_change_date_time'), 'base_currency_change_history', ['change_date_time'], unique=False)
    op.create_table('user_categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('is_income', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['user_categories.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_categories_name'), 'user_categories', ['name'], unique=False)
    op.create_index(op.f('ix_user_categories_parent_id'), 'user_categories', ['parent_id'], unique=False)
    op.create_index(op.f('ix_user_categories_user_id'), 'user_categories', ['user_id'], unique=False)
    op.create_table('credit_account_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('own_balance', sa.Numeric(), nullable=True),
    sa.Column('credit_balance', sa.Numeric(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('currency_id', sa.Integer(), nullable=True),
    sa.Column('amount_in_currency', sa.Numeric(), nullable=True),
    sa.Column('short_description', sa.String(length=50), nullable=True),
    sa.Column('long_description', sa.String(), nullable=True),
    sa.Column('datetime', sa.DateTime(timezone=True), nullable=True),
    sa.Column('exchange_rate', sa.Numeric(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), server_default='f', nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['user_categories.id'], ),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_account_id'), 'transactions', ['account_id'], unique=False)
    op.create_index(op.f('ix_transactions_category_id'), 'transactions', ['category_id'], unique=False)
    op.create_index(op.f('ix_transactions_currency_id'), 'transactions', ['currency_id'], unique=False)
    op.create_index(op.f('ix_transactions_datetime'), 'transactions', ['datetime'], unique=False)
    op.create_index(op.f('ix_transactions_short_description'), 'transactions', ['short_description'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transactions_short_description'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_datetime'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_currency_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_category_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_account_id'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_table('credit_account_details')
    op.drop_index(op.f('ix_user_categories_user_id'), table_name='user_categories')
    op.drop_index(op.f('ix_user_categories_parent_id'), table_name='user_categories')
    op.drop_index(op.f('ix_user_categories_name'), table_name='user_categories')
    op.drop_table('user_categories')
    op.drop_index(op.f('ix_base_currency_change_history_change_date_time'), table_name='base_currency_change_history')
    op.drop_table('base_currency_change_history')
    op.drop_index(op.f('ix_accounts_user_id'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_name'), table_name='accounts')
    op.drop_table('accounts')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_exchange_rates_datetime'), table_name='exchange_rates')
    op.drop_table('exchange_rates')
    op.drop_index(op.f('ix_default_categories_name'), table_name='default_categories')
    op.drop_table('default_categories')
    op.drop_index(op.f('ix_currencies_name'), table_name='currencies')
    op.drop_index(op.f('ix_currencies_code'), table_name='currencies')
    op.drop_table('currencies')
    op.drop_index(op.f('ix_account_types_type_name'), table_name='account_types')
    op.drop_table('account_types')
    # ### end Alembic commands ###