"""Create users table

Revision ID: 001
Revises: None
Create Date: 2025-04-15

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), server_default='TENANT'),
        sa.Column('wallet_address', sa.String(255), unique=True, nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='1'),
        sa.Column('is_verified', sa.Boolean(), server_default='0'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    
    # Create indexes for common queries
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_wallet', 'users', ['wallet_address'])
    op.create_index('idx_users_role', 'users', ['role'])


def downgrade():
    # Drop indexes
    op.drop_index('idx_users_email')
    op.drop_index('idx_users_wallet')
    op.drop_index('idx_users_role')
    
    # Drop the table
    op.drop_table('users') 