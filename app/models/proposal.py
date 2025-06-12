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
    CONFIRMED = "confirmed"


class Proposal(Base):
    """Proposal model representing rental proposals from tenants to landlords."""
    
    __tablename__ = "proposals"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_signature = Column(String(255), nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    price_offer = Column(Numeric(10, 2), nullable=False)
    message = Column(Text, nullable=True)
    status = Column(
        String(20),
        default=ProposalStatus.PENDING.value,
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmation_tx_hash = Column(String(255), nullable=True)
    metadata_uri = Column(String(255), nullable=True)
    
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

# --- Pydantic Schemas --- 

from pydantic import BaseModel, Field
from typing import Optional


class ProposalBase(BaseModel):
    """Base schema for proposal data."""
    property_id: str
    start_date: datetime
    end_date: datetime
    price_offer: float # Assuming direct float mapping is okay
    message: Optional[str] = None
    tenant_signature: Optional[str] = None # If implemented

    class Config:
        orm_mode = True # Enable mapping from SQLAlchemy model


class ProposalCreate(ProposalBase):
    """Schema for creating a new proposal (tenant provides this)."""
    pass # Inherits all fields from ProposalBase


class ProposalUpdateStatus(BaseModel):
    """Schema for updating proposal status (e.g., accept, reject, cancel)."""
    status: ProposalStatus


class ProposalResponse(ProposalBase):
    """Schema for returning proposal data to the client."""
    id: str # Use the string UUID from the model
    tenant_id: str
    status: ProposalStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    confirmation_tx_hash: Optional[str] = None
    metadata_uri: Optional[str] = None
    
    # Include related data if needed (requires configuration in endpoint)
    # property: Optional[PropertyResponse] = None # Example
    # tenant: Optional[UserResponse] = None      # Example

    class Config:
        orm_mode = True 