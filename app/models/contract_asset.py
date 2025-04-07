"""
ContractAsset model for the database.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, Numeric, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class ContractStatus(str, enum.Enum):
    """Contract status enumeration."""
    DRAFT = "draft"
    SIGNED = "signed"
    ACTIVE = "active"
    COMPLETED = "completed"
    TERMINATED = "terminated"
    DISPUTED = "disputed"


class ContractAsset(Base):
    """ContractAsset model representing rental agreements on the blockchain."""
    
    __tablename__ = "contract_assets"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    property_id = Column(
        String(36),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False
    )
    term = Column(Numeric(5, 0), nullable=False)  # Duration in months
    initial_date = Column(DateTime, nullable=False)
    final_date = Column(DateTime, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    conditions = Column(Text, nullable=True)
    blockchain_id = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(
        String(20),
        default=ContractStatus.DRAFT.value,
        nullable=False
    )
    
    # Foreign keys
    landlord_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    tenant_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Digital signatures
    landlord_signature = Column(String(255), nullable=True)
    tenant_signature = Column(String(255), nullable=True)
    
    # Relationships
    property = relationship("Property", backref="contracts")
    landlord = relationship("User", foreign_keys=[landlord_id], backref="landlord_contracts")
    tenant = relationship("User", foreign_keys=[tenant_id], backref="tenant_contracts")
    payments = relationship("Transaction", backref="contract")
    
    def __repr__(self):
        return f"<ContractAsset {self.id}: {self.property_id} - {self.status}>" 