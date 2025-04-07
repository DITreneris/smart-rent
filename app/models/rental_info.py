"""
RentalInfo model for the database.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class RentalStatus(str, enum.Enum):
    """Rental status enumeration."""
    ACTIVE = "active"
    PENDING = "pending"
    COMPLETED = "completed"
    TERMINATED = "terminated"


class RentalInfo(Base):
    """RentalInfo model for storing information about property rentals."""
    
    __tablename__ = "rental_info"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    property_id = Column(
        String(36),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False
    )
    tenant_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    initial_date = Column(DateTime, nullable=False)
    final_date = Column(DateTime, nullable=False)
    highest_proposal_id = Column(
        String(36),
        ForeignKey("proposals.id", ondelete="SET NULL"),
        nullable=True
    )
    number_of_proposals = Column(Integer, default=0)
    monthly_price = Column(Numeric(10, 2), nullable=False)
    security_deposit = Column(Numeric(10, 2), nullable=True)
    is_active = Column(Boolean, default=False)
    status = Column(
        String(20),
        default=RentalStatus.PENDING.value,
        nullable=False
    )
    blockchain_tx_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", backref="rental_info")
    tenant = relationship("User", backref="rentals")
    highest_proposal = relationship("Proposal", backref="selected_for")
    
    def __repr__(self):
        return f"<RentalInfo {self.id}: {self.property_id} - {self.status}>" 