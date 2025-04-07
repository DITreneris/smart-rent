"""
PropertyPhoto model for the database.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class PropertyPhoto(Base):
    """PropertyPhoto model for storing property images."""
    
    __tablename__ = "property_photos"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    property_id = Column(
        String(36),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False
    )
    photo_url = Column(String(255), nullable=True)
    photo_data = Column(LargeBinary, nullable=True)  # For storing images directly in DB if needed
    content_type = Column(String(100), nullable=True)  # MIME type
    filename = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    is_primary = Column(String(1), default="0")  # 0 = no, 1 = yes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", backref="photos")
    
    def __repr__(self):
        return f"<PropertyPhoto {self.id}: {self.property_id}>" 