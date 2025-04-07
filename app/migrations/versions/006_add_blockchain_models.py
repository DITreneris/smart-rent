"""
Add blockchain models migration.
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade():
    # Create proposals table
    op.create_table(
        'proposals',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('tenant_signature', sa.String(255), nullable=True),
        sa.Column('contract_id', sa.String(255), nullable=True),
        sa.Column('start_date', sa.DateTime, nullable=False),
        sa.Column('end_date', sa.DateTime, nullable=False),
        sa.Column('price_offer', sa.Numeric(10, 2), nullable=False),
        sa.Column('message', sa.Text, nullable=True),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('status', sa.String(20), nullable=False, default='pending'),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('blockchain_tx_id', sa.String(255), nullable=True),
        sa.Column('meta_data', sa.JSON, nullable=True),
        sa.Column('property_id', sa.String(36), nullable=False),
        sa.Column('tenant_id', sa.String(36), nullable=False),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tenant_id'], ['users.id'], ondelete='CASCADE')
    )

    # Create contract_assets table
    op.create_table(
        'contract_assets',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('property_id', sa.String(36), nullable=False),
        sa.Column('term', sa.Numeric(5, 0), nullable=False),
        sa.Column('initial_date', sa.DateTime, nullable=False),
        sa.Column('final_date', sa.DateTime, nullable=False),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('conditions', sa.Text, nullable=True),
        sa.Column('blockchain_id', sa.String(255), unique=True, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('status', sa.String(20), nullable=False, default='draft'),
        sa.Column('landlord_id', sa.String(36), nullable=False),
        sa.Column('tenant_id', sa.String(36), nullable=True),
        sa.Column('landlord_signature', sa.String(255), nullable=True),
        sa.Column('tenant_signature', sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['landlord_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tenant_id'], ['users.id'], ondelete='SET NULL')
    )

    # Create property_photos table
    op.create_table(
        'property_photos',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('property_id', sa.String(36), nullable=False),
        sa.Column('photo_url', sa.String(255), nullable=True),
        sa.Column('photo_data', sa.LargeBinary, nullable=True),
        sa.Column('content_type', sa.String(100), nullable=True),
        sa.Column('filename', sa.String(255), nullable=True),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('is_primary', sa.String(1), default='0'),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='CASCADE')
    )

    # Create rental_info table
    op.create_table(
        'rental_info',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('property_id', sa.String(36), nullable=False),
        sa.Column('tenant_id', sa.String(36), nullable=True),
        sa.Column('initial_date', sa.DateTime, nullable=False),
        sa.Column('final_date', sa.DateTime, nullable=False),
        sa.Column('highest_proposal_id', sa.String(36), nullable=True),
        sa.Column('number_of_proposals', sa.Integer, default=0),
        sa.Column('monthly_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('security_deposit', sa.Numeric(10, 2), nullable=True),
        sa.Column('is_active', sa.Boolean, default=False),
        sa.Column('status', sa.String(20), nullable=False, default='pending'),
        sa.Column('blockchain_tx_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tenant_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['highest_proposal_id'], ['proposals.id'], ondelete='SET NULL')
    )

    # Create payments table
    op.create_table(
        'payments',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('contract_id', sa.String(36), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('token_type', sa.String(50), nullable=True, default='ETH'),
        sa.Column('token_address', sa.String(255), nullable=True),
        sa.Column('payment_date', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('expiration_time', sa.DateTime, nullable=True),
        sa.Column('transaction_hash', sa.String(255), nullable=True, unique=True),
        sa.Column('first_payment_status', sa.String(20), nullable=False, default='pending'),
        sa.Column('next_payment_status', sa.String(20), nullable=True),
        sa.Column('final_payment_date', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('payment_description', sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(['contract_id'], ['contract_assets.id'], ondelete='CASCADE')
    )

    # Create documents table
    op.create_table(
        'documents',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('encrypted_id', sa.String(255), nullable=True),
        sa.Column('document_hash', sa.String(255), nullable=True),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('content_type', sa.String(100), nullable=True),
        sa.Column('document_url', sa.String(255), nullable=True),
        sa.Column('document_data', sa.LargeBinary, nullable=True),
        sa.Column('encryption_method', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('document_type', sa.String(20), nullable=False, default='other'),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('blockchain_tx_id', sa.String(255), nullable=True),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('property_id', sa.String(36), nullable=True),
        sa.Column('contract_id', sa.String(36), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['contract_id'], ['contract_assets.id'], ondelete='SET NULL')
    )

    # Add contract_id to transactions table
    op.add_column(
        'transactions', 
        sa.Column('contract_id', sa.String(36), nullable=True)
    )
    
    op.create_foreign_key(
        'fk_transactions_contract',
        'transactions',
        'contract_assets',
        ['contract_id'],
        ['id'],
        ondelete='SET NULL'
    )


def downgrade():
    # Remove contract_id from transactions
    op.drop_constraint('fk_transactions_contract', 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'contract_id')
    
    # Drop tables in reverse order of creation (respecting foreign key constraints)
    op.drop_table('documents')
    op.drop_table('payments')
    op.drop_table('rental_info')
    op.drop_table('property_photos')
    op.drop_table('contract_assets')
    op.drop_table('proposals') 