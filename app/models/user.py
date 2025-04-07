"""
User model for the database.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "ADMIN"
    LANDLORD = "LANDLORD"
    TENANT = "TENANT"


class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(
        String(20),
        default=UserRole.TENANT.value,
        nullable=False
    )
    wallet_address = Column(String(255), unique=True, nullable=True)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    properties = relationship("Property", back_populates="owner")
    
    def __repr__(self):
        return f"<User {self.id}: {self.email} - {self.role}>" 