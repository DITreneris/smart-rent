from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    price: float
    bedrooms: int
    bathrooms: float
    area: Optional[float] = None
    image_urls: Optional[str] = None
    available: bool = True

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    area: Optional[float] = None
    image_urls: Optional[str] = None
    available: Optional[bool] = None
    blockchain_id: Optional[str] = None

class PropertyInDBBase(PropertyBase):
    id: str
    owner_id: str
    blockchain_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Property(PropertyInDBBase):
    pass

class PropertyWithOwner(Property):
    owner: "User" 