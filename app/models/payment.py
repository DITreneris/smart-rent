"""
Payment model for the database.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class PaymentStatus(str, enum.Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    """Payment model for storing blockchain payment records."""
    
    __tablename__ = "payments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    contract_id = Column(
        String(36),
        ForeignKey("contract_assets.id", ondelete="CASCADE"),
        nullable=False
    )
    amount = Column(Numeric(10, 2), nullable=False)
    token_type = Column(String(50), nullable=True, default="ETH")
    token_address = Column(String(255), nullable=True)
    payment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    expiration_time = Column(DateTime, nullable=True)
    transaction_hash = Column(String(255), nullable=True, unique=True)
    first_payment_status = Column(
        String(20),
        default=PaymentStatus.PENDING.value,
        nullable=False
    )
    next_payment_status = Column(
        String(20),
        nullable=True
    )
    final_payment_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    payment_description = Column(String(255), nullable=True)
    
    # Relationships
    contract = relationship("ContractAsset", backref="payment_records")
    
    def __repr__(self):
        return f"<Payment {self.id}: {self.contract_id} - {self.amount}>" 