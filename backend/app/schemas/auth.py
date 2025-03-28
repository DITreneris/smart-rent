from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    TENANT = "tenant"
    LANDLORD = "landlord"
    ADMIN = "admin"


class UserStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    wallet_address: Optional[str] = None


class UserResponse(UserBase):
    id: int
    role: UserRole
    status: UserStatus
    wallet_address: Optional[str] = None
    documents: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class DocumentUpload(BaseModel):
    document_urls: Dict[str, str] 