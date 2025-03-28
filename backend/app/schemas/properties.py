from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class PropertyStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    RENTED = "rented"


class PropertyBase(BaseModel):
    title: str
    description: str
    address: str
    price: int  # Monthly rent in smallest currency unit


class PropertyCreate(PropertyBase):
    images: Optional[List[str]] = None
    features: Optional[Dict[str, Any]] = None


class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    price: Optional[int] = None
    images: Optional[List[str]] = None
    features: Optional[Dict[str, Any]] = None


class PropertyResponse(PropertyBase):
    id: int
    owner_id: int
    status: PropertyStatus
    images: Optional[List[str]] = None
    features: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True 