"""
Transaction model for the database.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class TransactionStatus(str, enum.Enum):
    """Transaction status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TransactionType(str, enum.Enum):
    """Transaction type enumeration."""
    RENT = "rent"
    DEPOSIT = "deposit"
    DEPOSIT_RETURN = "deposit_return"
    MAINTENANCE = "maintenance"
    OTHER = "other"


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