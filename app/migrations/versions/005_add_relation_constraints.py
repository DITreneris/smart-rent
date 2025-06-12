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
    # Add ON DELETE CASCADE for property owner relation using explicit FK name
    with op.batch_alter_table('properties', schema=None) as batch_op:
        # batch_op.drop_constraint('properties_ibfk_1', type_='foreignkey') # Don't drop if name is unknown/auto-generated
        batch_op.create_foreign_key(
            'fk_property_owner', # Explicit name
            'users',
            ['owner_id'], ['id'],
            ondelete='CASCADE'
        )
    
    # Add ON DELETE CASCADE for transaction user relation using explicit FK name
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        # batch_op.drop_constraint('transactions_ibfk_1', type_='foreignkey') # Don't drop if name is unknown/auto-generated
        batch_op.create_foreign_key(
            'fk_transaction_user', # Explicit name
            'users',
            ['user_id'], ['id'],
            ondelete='CASCADE'
        )
    
    # Make property_id nullable and add ON DELETE SET NULL for transaction property relation
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        # batch_op.drop_constraint('transactions_ibfk_2', type_='foreignkey') # Don't drop if name is unknown/auto-generated
        batch_op.alter_column('property_id', existing_type=sa.String(36), nullable=True)
        batch_op.create_foreign_key(
            'fk_transaction_property', # Explicit name
            'properties',
            ['property_id'], ['id'],
            ondelete='SET NULL'
        )
    
    # Create rental_agreements table (fix ON UPDATE clause)
    op.create_table(
        'rental_agreements',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('property_id', sa.String(36), sa.ForeignKey('properties.id', name='fk_rental_property', ondelete='CASCADE'), nullable=False), # Added name
        sa.Column('tenant_id', sa.String(36), sa.ForeignKey('users.id', name='fk_rental_tenant', ondelete='CASCADE'), nullable=False), # Added name
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(20), server_default='pending'),
        sa.Column('monthly_rent', sa.Numeric(10, 2), nullable=False),
        sa.Column('security_deposit', sa.Numeric(10, 2), nullable=False),
        sa.Column('agreement_hash', sa.String(255), nullable=True),
        sa.Column('blockchain_id', sa.String(255), unique=True, nullable=True),
        sa.Column('metadata', sa.JSON),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        # Removed 'ON UPDATE CURRENT_TIMESTAMP' for SQLite compatibility
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    
    # Create indexes for rental agreements
    op.create_index('idx_rental_property', 'rental_agreements', ['property_id'])
    op.create_index('idx_rental_tenant', 'rental_agreements', ['tenant_id'])
    op.create_index('idx_rental_status', 'rental_agreements', ['status'])
    op.create_index('idx_rental_dates', 'rental_agreements', ['start_date', 'end_date'])
    
    # Add check constraints to rental_agreements using batch mode
    with op.batch_alter_table('rental_agreements', schema=None) as batch_op:
        batch_op.create_check_constraint('check_rental_dates_valid', 'end_date > start_date')
        batch_op.create_check_constraint('check_rental_rent_positive', 'monthly_rent > 0')
        batch_op.create_check_constraint('check_rental_deposit_positive', 'security_deposit >= 0')


def downgrade():
    # Drop rental_agreements table constraints using batch mode
    with op.batch_alter_table('rental_agreements', schema=None) as batch_op:
        batch_op.drop_constraint('check_rental_dates_valid', type_='check')
        batch_op.drop_constraint('check_rental_rent_positive', type_='check')
        batch_op.drop_constraint('check_rental_deposit_positive', type_='check')
    
    # Drop indexes (no batch mode needed for indexes)
    op.drop_index('idx_rental_property', table_name='rental_agreements')
    op.drop_index('idx_rental_tenant', table_name='rental_agreements')
    op.drop_index('idx_rental_status', table_name='rental_agreements')
    op.drop_index('idx_rental_dates', table_name='rental_agreements')
    
    # Drop table (no batch mode needed)
    op.drop_table('rental_agreements')
    
    # Restore original foreign keys and NOT NULL constraint using explicit names
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_constraint('fk_transaction_property', type_='foreignkey')
        batch_op.alter_column('property_id', existing_type=sa.String(36), nullable=False)
        # Cannot reliably recreate the original unnamed constraint, maybe omit or add simple FK?
        # batch_op.create_foreign_key(None, 'properties', ['property_id'], ['id'])
        
        batch_op.drop_constraint('fk_transaction_user', type_='foreignkey')
        # Cannot reliably recreate the original unnamed constraint, maybe omit or add simple FK?
        # batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])
    
    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.drop_constraint('fk_property_owner', type_='foreignkey')
        # Cannot reliably recreate the original unnamed constraint, maybe omit or add simple FK?
        # batch_op.create_foreign_key(None, 'users', ['owner_id'], ['id']) 