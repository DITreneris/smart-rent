"""Create transactions table

Revision ID: 003
Revises: 002
Create Date: 2025-04-15

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # Create transactions table
    op.create_table(
        'transactions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('hash', sa.String(255), unique=True, nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('type', sa.String(20), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('from_address', sa.String(255), nullable=True),
        sa.Column('to_address', sa.String(255), nullable=True),
        sa.Column('confirmations', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('error', sa.String(255), nullable=True),
        sa.Column('transaction_data', sa.JSON),
        sa.Column('receipt_url', sa.String(255), nullable=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('property_id', sa.String(36), sa.ForeignKey('properties.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )
    
    # Create indexes for common queries
    op.create_index('idx_transactions_user', 'transactions', ['user_id'])
    op.create_index('idx_transactions_property', 'transactions', ['property_id'])
    op.create_index('idx_transactions_status', 'transactions', ['status'])
    op.create_index('idx_transactions_hash', 'transactions', ['hash'])
    op.create_index('idx_transactions_type', 'transactions', ['type'])


def downgrade():
    # Drop indexes
    op.drop_index('idx_transactions_user')
    op.drop_index('idx_transactions_property')
    op.drop_index('idx_transactions_status')
    op.drop_index('idx_transactions_hash')
    op.drop_index('idx_transactions_type')
    
    # Drop the table
    op.drop_table('transactions') 