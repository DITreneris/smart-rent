"""Create property table

Revision ID: 002
Revises: 001
Create Date: 2025-04-15

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'properties',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('bedrooms', sa.Numeric(3, 1), server_default='1'),
        sa.Column('bathrooms', sa.Numeric(3, 1), server_default='1'),
        sa.Column('area', sa.Numeric(10, 2)),
        sa.Column('amenities', sa.JSON),
        sa.Column('images', sa.JSON),
        sa.Column('address', sa.JSON),
        sa.Column('blockchain_id', sa.String(255), unique=True, nullable=True),
        sa.Column('metadata_uri', sa.String(255), nullable=True),
        sa.Column('status', sa.String(20), server_default='available'),
        sa.Column('owner_id', sa.String(36), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    
    # Create indexes for common queries
    op.create_index('idx_properties_owner', 'properties', ['owner_id'])
    op.create_index('idx_properties_status', 'properties', ['status'])
    op.create_index('idx_properties_price', 'properties', ['price'])
    op.create_index('idx_properties_blockchain_id', 'properties', ['blockchain_id'])


def downgrade():
    # Drop indexes
    op.drop_index('idx_properties_owner')
    op.drop_index('idx_properties_status')
    op.drop_index('idx_properties_price')
    op.drop_index('idx_properties_blockchain_id')
    
    # Drop the table
    op.drop_table('properties') 