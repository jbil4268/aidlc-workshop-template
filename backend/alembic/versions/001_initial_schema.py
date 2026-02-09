"""initial schema

Revision ID: 001
Revises: 
Create Date: 2026-02-09

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create stores table
    op.create_table(
        'stores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stores_id'), 'stores', ['id'], unique=False)

    # Create tables table
    op.create_table(
        'tables',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('store_id', sa.Integer(), nullable=False),
        sa.Column('table_number', sa.String(length=20), nullable=False),
        sa.Column('qr_code', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tables_id'), 'tables', ['id'], unique=False)
    op.create_index(op.f('ix_tables_store_id'), 'tables', ['store_id'], unique=False)
    op.create_index(op.f('ix_tables_qr_code'), 'tables', ['qr_code'], unique=True)

    # Create table_sessions table
    op.create_table(
        'table_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('table_id', sa.Integer(), nullable=False),
        sa.Column('session_token', sa.String(length=255), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('ended_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['table_id'], ['tables.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_table_sessions_id'), 'table_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_table_sessions_table_id'), 'table_sessions', ['table_id'], unique=False)
    op.create_index(op.f('ix_table_sessions_session_token'), 'table_sessions', ['session_token'], unique=True)

    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('store_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_index(op.f('ix_categories_store_id'), 'categories', ['store_id'], unique=False)

    # Create menus table
    op.create_table(
        'menus',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('allergens', sa.String(length=255), nullable=True),
        sa.Column('is_available', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menus_id'), 'menus', ['id'], unique=False)
    op.create_index(op.f('ix_menus_category_id'), 'menus', ['category_id'], unique=False)

    # Create orders table
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('order_number', sa.String(length=20), nullable=False),
        sa.Column('subtotal_amount', sa.Integer(), nullable=False),
        sa.Column('tip_rate', sa.Integer(), nullable=False),
        sa.Column('tip_amount', sa.Integer(), nullable=False),
        sa.Column('total_amount', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'PREPARING', 'READY', 'SERVED', 'CANCELLED', name='orderstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['table_sessions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)
    op.create_index(op.f('ix_orders_session_id'), 'orders', ['session_id'], unique=False)
    op.create_index(op.f('ix_orders_order_number'), 'orders', ['order_number'], unique=False)
    op.create_index(op.f('ix_orders_status'), 'orders', ['status'], unique=False)
    op.create_index(op.f('ix_orders_created_at'), 'orders', ['created_at'], unique=False)

    # Create order_items table
    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('menu_id', sa.Integer(), nullable=False),
        sa.Column('menu_name', sa.String(length=100), nullable=False),
        sa.Column('menu_price', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('subtotal', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_items_id'), 'order_items', ['id'], unique=False)
    op.create_index(op.f('ix_order_items_order_id'), 'order_items', ['order_id'], unique=False)
    op.create_index(op.f('ix_order_items_menu_id'), 'order_items', ['menu_id'], unique=False)

    # Create admins table
    op.create_table(
        'admins',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('store_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admins_id'), 'admins', ['id'], unique=False)
    op.create_index(op.f('ix_admins_store_id'), 'admins', ['store_id'], unique=False)
    op.create_index(op.f('ix_admins_username'), 'admins', ['username'], unique=True)

    # Create order_history table
    op.create_table(
        'order_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('old_status', sa.String(length=20), nullable=False),
        sa.Column('new_status', sa.String(length=20), nullable=False),
        sa.Column('changed_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_history_id'), 'order_history', ['id'], unique=False)
    op.create_index(op.f('ix_order_history_order_id'), 'order_history', ['order_id'], unique=False)
    op.create_index(op.f('ix_order_history_changed_at'), 'order_history', ['changed_at'], unique=False)


def downgrade() -> None:
    op.drop_table('order_history')
    op.drop_table('admins')
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_table('menus')
    op.drop_table('categories')
    op.drop_table('table_sessions')
    op.drop_table('tables')
    op.drop_table('stores')
