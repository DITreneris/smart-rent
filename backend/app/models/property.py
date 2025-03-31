from sqlalchemy import Column, String, Text, Numeric, ForeignKey, DateTime, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.db.base_class import Base

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Numeric, nullable=False)
    bedrooms = Column(Numeric, default=1)
    bathrooms = Column(Numeric, default=1)
    area = Column(Numeric)
    amenities = Column(JSON, default=list)
    images = Column(JSON, default=list)
    
    address = Column(JSON)
    blockchain_id = Column(String, unique=True, nullable=True)
    metadataURI = Column(String, nullable=True)
    
    status = Column(
        Enum("available", "rented", "pending", name="property_status"),
        default="available"
    )
    
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 