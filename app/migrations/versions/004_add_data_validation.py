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
    op.create_check_constraint(
        'check_property_price_positive',
        'properties',
        'price > 0'
    )
    
    op.create_check_constraint(
        'check_property_bedrooms_positive',
        'properties',
        'bedrooms > 0'
    )
    
    op.create_check_constraint(
        'check_property_bathrooms_positive',
        'properties',
        'bathrooms > 0'
    )
    
    op.create_check_constraint(
        'check_property_area_positive',
        'properties',
        'area > 0'
    )
    
    # Add validation constraints to users table
    op.create_check_constraint(
        'check_user_email_format',
        'users',
        "email REGEXP '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'"
    )
    
    op.create_check_constraint(
        'check_user_wallet_format',
        'users',
        "wallet_address IS NULL OR wallet_address REGEXP '^0x[a-fA-F0-9]{40}$'"
    )
    
    # Add validation constraints to transactions table
    op.create_check_constraint(
        'check_transaction_hash_format',
        'transactions',
        "hash IS NULL OR hash REGEXP '^0x[a-fA-F0-9]{64}$'"
    )
    
    op.create_check_constraint(
        'check_transaction_from_address_format',
        'transactions',
        "from_address IS NULL OR from_address REGEXP '^0x[a-fA-F0-9]{40}$'"
    )
    
    op.create_check_constraint(
        'check_transaction_to_address_format',
        'transactions',
        "to_address IS NULL OR to_address REGEXP '^0x[a-fA-F0-9]{40}$'"
    )
    
    op.create_check_constraint(
        'check_transaction_confirmations_positive',
        'transactions',
        'confirmations IS NULL OR confirmations >= 0'
    )


def downgrade():
    # Drop constraints from properties table
    op.drop_constraint('check_property_price_positive', 'properties', type_='check')
    op.drop_constraint('check_property_bedrooms_positive', 'properties', type_='check')
    op.drop_constraint('check_property_bathrooms_positive', 'properties', type_='check')
    op.drop_constraint('check_property_area_positive', 'properties', type_='check')
    
    # Drop constraints from users table
    op.drop_constraint('check_user_email_format', 'users', type_='check')
    op.drop_constraint('check_user_wallet_format', 'users', type_='check')
    
    # Drop constraints from transactions table
    op.drop_constraint('check_transaction_hash_format', 'transactions', type_='check')
    op.drop_constraint('check_transaction_from_address_format', 'transactions', type_='check')
    op.drop_constraint('check_transaction_to_address_format', 'transactions', type_='check')
    op.drop_constraint('check_transaction_confirmations_positive', 'transactions', type_='check') 