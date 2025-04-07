"""Add relation constraints between tables

Revision ID: 005
Revises: 004
Create Date: 2025-04-15

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade():
    # Add ON DELETE CASCADE for property owner relation
    with op.batch_alter_table('properties') as batch_op:
        batch_op.drop_constraint('properties_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_property_owner',
            'users',
            ['owner_id'], ['id'],
            ondelete='CASCADE'
        )
    
    # Add ON DELETE CASCADE for transaction user relation
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.drop_constraint('transactions_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_transaction_user',
            'users',
            ['user_id'], ['id'],
            ondelete='CASCADE'
        )
    
    # Make property_id nullable and add ON DELETE SET NULL for transaction property relation
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.drop_constraint('transactions_ibfk_2', type_='foreignkey')
        batch_op.alter_column('property_id', existing_type=sa.String(36), nullable=True)
        batch_op.create_foreign_key(
            'fk_transaction_property',
            'properties',
            ['property_id'], ['id'],
            ondelete='SET NULL'
        )
    
    # Create rental_agreements table
    op.create_table(
        'rental_agreements',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('property_id', sa.String(36), sa.ForeignKey('properties.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tenant_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(20), server_default='pending'),
        sa.Column('monthly_rent', sa.Numeric(10, 2), nullable=False),
        sa.Column('security_deposit', sa.Numeric(10, 2), nullable=False),
        sa.Column('agreement_hash', sa.String(255), nullable=True),
        sa.Column('blockchain_id', sa.String(255), unique=True, nullable=True),
        sa.Column('metadata', sa.JSON),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
    )
    
    # Create indexes for rental agreements
    op.create_index('idx_rental_property', 'rental_agreements', ['property_id'])
    op.create_index('idx_rental_tenant', 'rental_agreements', ['tenant_id'])
    op.create_index('idx_rental_status', 'rental_agreements', ['status'])
    op.create_index('idx_rental_dates', 'rental_agreements', ['start_date', 'end_date'])
    
    # Add check constraints to rental_agreements
    op.create_check_constraint(
        'check_rental_dates_valid',
        'rental_agreements',
        'end_date > start_date'
    )
    
    op.create_check_constraint(
        'check_rental_rent_positive',
        'rental_agreements',
        'monthly_rent > 0'
    )
    
    op.create_check_constraint(
        'check_rental_deposit_positive',
        'rental_agreements',
        'security_deposit >= 0'
    )


def downgrade():
    # Drop rental_agreements table and its constraints
    op.drop_constraint('check_rental_dates_valid', 'rental_agreements', type_='check')
    op.drop_constraint('check_rental_rent_positive', 'rental_agreements', type_='check')
    op.drop_constraint('check_rental_deposit_positive', 'rental_agreements', type_='check')
    
    op.drop_index('idx_rental_property', 'rental_agreements')
    op.drop_index('idx_rental_tenant', 'rental_agreements')
    op.drop_index('idx_rental_status', 'rental_agreements')
    op.drop_index('idx_rental_dates', 'rental_agreements')
    
    op.drop_table('rental_agreements')
    
    # Restore original foreign keys and NOT NULL constraint
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.drop_constraint('fk_transaction_property', type_='foreignkey')
        batch_op.alter_column('property_id', existing_type=sa.String(36), nullable=False)
        batch_op.create_foreign_key(
            'transactions_ibfk_2',
            'properties',
            ['property_id'], ['id']
        )
        
        batch_op.drop_constraint('fk_transaction_user', type_='foreignkey')
        batch_op.create_foreign_key(
            'transactions_ibfk_1',
            'users',
            ['user_id'], ['id']
        )
    
    with op.batch_alter_table('properties') as batch_op:
        batch_op.drop_constraint('fk_property_owner', type_='foreignkey')
        batch_op.create_foreign_key(
            'properties_ibfk_1',
            'users',
            ['owner_id'], ['id']
        ) 