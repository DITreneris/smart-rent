"""Add data validation constraints

Revision ID: 004
Revises: 003
Create Date: 2025-04-15

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Add validation constraints to properties table
    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.create_check_constraint('check_property_price_positive', 'price > 0')
        batch_op.create_check_constraint('check_property_bedrooms_positive', 'bedrooms > 0')
        batch_op.create_check_constraint('check_property_bathrooms_positive', 'bathrooms > 0')
        batch_op.create_check_constraint('check_property_area_positive', 'area > 0')

    # Add validation constraints to users table
    with op.batch_alter_table('users', schema=None) as batch_op:
        # Note: REGEXP might not be available by default in SQLite, depending on compilation.
        # Consider alternative validation if this fails, or ensure REGEXP support.
        batch_op.create_check_constraint('check_user_email_format', "email LIKE '%_@__%.__%'") # Simplified LIKE pattern
        batch_op.create_check_constraint('check_user_wallet_format', "wallet_address IS NULL OR (wallet_address LIKE '0x%' AND length(wallet_address) = 42)") # Simplified check

    # Add validation constraints to transactions table
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        # Note: REGEXP might not be available by default in SQLite.
        batch_op.create_check_constraint('check_transaction_hash_format', "hash IS NULL OR (hash LIKE '0x%' AND length(hash) = 66)") # Simplified check
        batch_op.create_check_constraint('check_transaction_from_address_format', "from_address IS NULL OR (from_address LIKE '0x%' AND length(from_address) = 42)") # Simplified check
        batch_op.create_check_constraint('check_transaction_to_address_format', "to_address IS NULL OR (to_address LIKE '0x%' AND length(to_address) = 42)") # Simplified check
        batch_op.create_check_constraint('check_transaction_confirmations_positive', 'confirmations IS NULL OR confirmations >= 0')


def downgrade():
    # Drop constraints from properties table
    with op.batch_alter_table('properties', schema=None) as batch_op:
        batch_op.drop_constraint('check_property_price_positive', type_='check')
        batch_op.drop_constraint('check_property_bedrooms_positive', type_='check')
        batch_op.drop_constraint('check_property_bathrooms_positive', type_='check')
        batch_op.drop_constraint('check_property_area_positive', type_='check')
    
    # Drop constraints from users table
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('check_user_email_format', type_='check')
        batch_op.drop_constraint('check_user_wallet_format', type_='check')
    
    # Drop constraints from transactions table
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_constraint('check_transaction_hash_format', type_='check')
        batch_op.drop_constraint('check_transaction_from_address_format', type_='check')
        batch_op.drop_constraint('check_transaction_to_address_format', type_='check')
        batch_op.drop_constraint('check_transaction_confirmations_positive', type_='check') 