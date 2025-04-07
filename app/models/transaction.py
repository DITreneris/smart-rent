"""
Transaction model for the database.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

from app.db.base import Base


class TransactionStatus(str, enum.Enum):
    """Enum for transaction status values."""
    PENDING = "pending"
    CONFIRMING = "confirming"
    CONFIRMED = "confirmed"
    VERIFIED = "verified"
    VERIFICATION_FAILED = "verification_failed"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class TransactionType(str, enum.Enum):
    """Transaction type enumeration."""
    RENT = "rent"
    DEPOSIT = "deposit"
    DEPOSIT_RETURN = "deposit_return"
    MAINTENANCE = "maintenance"
    OTHER = "other"


class VerificationResult(BaseModel):
    """Model for transaction verification results."""
    success: bool
    details: Dict[str, Any] = {}
    network_confirmations: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    

class TransactionBase(BaseModel):
    """Base transaction model."""
    tx_hash: str
    tx_type: str
    from_address: str
    to_address: str
    value: float
    currency: str
    status: TransactionStatus = TransactionStatus.PENDING
    network: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TransactionCreate(TransactionBase):
    """Model for creating a new transaction."""
    pass


class TransactionUpdate(BaseModel):
    """Model for updating a transaction."""
    status: Optional[TransactionStatus] = None
    confirmations: Optional[int] = None
    verified: Optional[bool] = None
    verification_result: Optional[Dict[str, Any]] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TransactionDB(TransactionBase):
    """Database model for transaction."""
    id: str
    confirmations: int = 0
    verified: bool = False
    verification_result: Optional[Dict[str, Any]] = None
    block_number: Optional[int] = None
    block_timestamp: Optional[datetime] = None
    gas_used: Optional[int] = None
    gas_price: Optional[float] = None
    fee: Optional[float] = None
    related_entity_id: Optional[str] = None
    related_entity_type: Optional[str] = None
    metadata: Dict[str, Any] = {}
    updated_at: Optional[datetime] = None


class TransactionResponse(TransactionDB):
    """API response model for transaction."""
    class Config:
        orm_mode = True


class Transaction(Base):
    """Transaction model."""
    
    __tablename__ = "transactions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hash = Column(String(255), unique=True, nullable=True)
    status = Column(
        String(20),
        default=TransactionStatus.PENDING.value,
        nullable=False
    )
    timestamp = Column(DateTime, nullable=False)
    description = Column(String(255))
    type = Column(
        String(20),
        nullable=False
    )
    amount = Column(Numeric(10, 2), nullable=False)
    from_address = Column(String(255), nullable=True)
    to_address = Column(String(255), nullable=True)
    confirmations = Column(Numeric(10, 0), default=0)
    error = Column(String(255), nullable=True)
    transaction_data = Column(JSON, nullable=True)
    receipt_url = Column(String(255), nullable=True)
    
    # Foreign keys
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    property_id = Column(
        String(36),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    property = relationship("Property", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction {self.id}: {self.type} - {self.status}>" 