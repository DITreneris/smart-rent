"""
Property model for the database.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, Numeric, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class PropertyStatus(str, enum.Enum):
    """Property status enumeration."""
    AVAILABLE = "available"
    RENTED = "rented"
    PENDING = "pending"
    MAINTENANCE = "maintenance"


class Property(Base):
    """Property model."""
    
    __tablename__ = "properties"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    bedrooms = Column(Numeric(3, 1), default=1)
    bathrooms = Column(Numeric(3, 1), default=1)
    area = Column(Numeric(10, 2))
    amenities = Column(JSON, default=list)
    images = Column(JSON, default=list)
    
    address = Column(JSON)
    blockchain_id = Column(String(255), unique=True, nullable=True)
    metadata_uri = Column(String(255), nullable=True)
    
    status = Column(
        String(20),
        default=PropertyStatus.AVAILABLE.value
    )
    
    # Foreign keys
    owner_id = Column(
        String(36), 
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Relationships
    owner = relationship("User", back_populates="properties")
    transactions = relationship("Transaction", back_populates="property")
    
    def __repr__(self):
        return f"<Property {self.id}: {self.title} - {self.status}>" 