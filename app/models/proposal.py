"""
Proposal model for the database.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, Numeric, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class ProposalStatus(str, enum.Enum):
    """Proposal status enumeration."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class Proposal(Base):
    """Proposal model representing rental proposals from tenants to landlords."""
    
    __tablename__ = "proposals"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_signature = Column(String(255), nullable=True)
    contract_id = Column(String(255), nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    price_offer = Column(Numeric(10, 2), nullable=False)
    message = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    status = Column(
        String(20),
        default=ProposalStatus.PENDING.value,
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    blockchain_tx_id = Column(String(255), nullable=True)
    meta_data = Column(JSON, nullable=True)
    
    # Foreign keys
    property_id = Column(
        String(36),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False
    )
    tenant_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Relationships
    property = relationship("Property", backref="proposals")
    tenant = relationship("User", backref="tenant_proposals")
    
    def __repr__(self):
        return f"<Proposal {self.id}: {self.property_id} - {self.status}>" 