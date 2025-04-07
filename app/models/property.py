"""
Property model for the database.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Text, Numeric, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator

from app.db.base import Base


class PropertyType(str, Enum):
    """Enum for property types."""
    APARTMENT = "apartment"
    HOUSE = "house"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    COMMERCIAL = "commercial"
    LAND = "land"
    OTHER = "other"


class PropertyStatus(str, Enum):
    """Enum for property status."""
    AVAILABLE = "available"
    RENTED = "rented"
    MAINTENANCE = "maintenance"
    PENDING = "pending"
    INACTIVE = "inactive"


class Address(BaseModel):
    """Model for property address."""
    street: str
    city: str
    state: str
    zip_code: str
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class PropertyImage(BaseModel):
    """Model for property images."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    url: str
    caption: Optional[str] = None
    is_primary: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PropertyFeature(BaseModel):
    """Model for property features."""
    name: str
    value: Any
    category: Optional[str] = None


class PropertyBase(BaseModel):
    """Base model for property."""
    title: str
    description: str
    property_type: PropertyType
    bedrooms: int
    bathrooms: float
    area: float  # square meters/feet
    price: float  # monthly rent
    currency: str = "USD"
    address: Address
    features: Optional[List[PropertyFeature]] = []
    status: PropertyStatus = PropertyStatus.AVAILABLE
    is_furnished: bool = False
    available_from: Optional[datetime] = None
    min_lease_duration: int = 1  # months
    max_lease_duration: Optional[int] = None  # months
    security_deposit: Optional[float] = None
    utilities_included: bool = False
    pets_allowed: bool = False
    smoking_allowed: bool = False
    metadata: Optional[Dict[str, Any]] = {}


class PropertyCreate(PropertyBase):
    """Model for creating a property."""
    owner_id: Optional[str] = None
    images: Optional[List[PropertyImage]] = []
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than zero')
        return v
    
    @validator('bedrooms')
    def validate_bedrooms(cls, v):
        if v < 0:
            raise ValueError('Bedrooms cannot be negative')
        return v
    
    @validator('bathrooms')
    def validate_bathrooms(cls, v):
        if v < 0:
            raise ValueError('Bathrooms cannot be negative')
        return v
    
    @validator('area')
    def validate_area(cls, v):
        if v <= 0:
            raise ValueError('Area must be greater than zero')
        return v


class PropertyUpdate(BaseModel):
    """Model for updating a property."""
    title: Optional[str] = None
    description: Optional[str] = None
    property_type: Optional[PropertyType] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    area: Optional[float] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    address: Optional[Address] = None
    features: Optional[List[PropertyFeature]] = None
    status: Optional[PropertyStatus] = None
    is_furnished: Optional[bool] = None
    available_from: Optional[datetime] = None
    min_lease_duration: Optional[int] = None
    max_lease_duration: Optional[int] = None
    security_deposit: Optional[float] = None
    utilities_included: Optional[bool] = None
    pets_allowed: Optional[bool] = None
    smoking_allowed: Optional[bool] = None
    images: Optional[List[PropertyImage]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @validator('price')
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Price must be greater than zero')
        return v
    
    @validator('bedrooms')
    def validate_bedrooms(cls, v):
        if v is not None and v < 0:
            raise ValueError('Bedrooms cannot be negative')
        return v
    
    @validator('bathrooms')
    def validate_bathrooms(cls, v):
        if v is not None and v < 0:
            raise ValueError('Bathrooms cannot be negative')
        return v
    
    @validator('area')
    def validate_area(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Area must be greater than zero')
        return v


class PropertyDB(PropertyBase):
    """Model for property in database."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    owner_id: str
    images: List[PropertyImage] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    blockchain_id: Optional[str] = None
    contract_address: Optional[str] = None
    verified: bool = False


class PropertyResponse(PropertyDB):
    """Model for property response."""
    class Config:
        orm_mode = True


class PropertySearchParams(BaseModel):
    """Model for property search parameters."""
    property_type: Optional[PropertyType] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_bedrooms: Optional[int] = None
    max_bedrooms: Optional[int] = None
    min_bathrooms: Optional[float] = None
    max_bathrooms: Optional[float] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    is_furnished: Optional[bool] = None
    available_from: Optional[datetime] = None
    status: Optional[PropertyStatus] = PropertyStatus.AVAILABLE
    pets_allowed: Optional[bool] = None
    utilities_included: Optional[bool] = None


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