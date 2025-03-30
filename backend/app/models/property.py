from sqlalchemy import Column, String, Float, Boolean, ForeignKey, Text, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.session import Base

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Float, nullable=False)
    area = Column(Float, nullable=True)  # in square feet
    image_urls = Column(String, nullable=True)  # JSON string of image URLs
    available = Column(Boolean, default=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    blockchain_id = Column(String, nullable=True)  # Property ID on blockchain
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="properties")
    leases = relationship("Lease", back_populates="property") 