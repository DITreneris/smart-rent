"""
Document model for the database.
"""

import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, LargeBinary, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class DocumentType(str, enum.Enum):
    """Document type enumeration."""
    CONTRACT = "contract"
    RECEIPT = "receipt"
    IDENTITY = "identity"
    PROPERTY = "property"
    OTHER = "other"


class Document(Base):
    """Document model for storing encrypted documents."""
    
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    encrypted_id = Column(String(255), nullable=True)
    document_hash = Column(String(255), nullable=True)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=True)
    document_url = Column(String(255), nullable=True)
    document_data = Column(LargeBinary, nullable=True)
    encryption_method = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    document_type = Column(
        String(20),
        default=DocumentType.OTHER.value,
        nullable=False
    )
    description = Column(Text, nullable=True)
    blockchain_tx_id = Column(String(255), nullable=True)
    
    # Foreign keys
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    property_id = Column(
        String(36),
        ForeignKey("properties.id", ondelete="SET NULL"),
        nullable=True
    )
    contract_id = Column(
        String(36),
        ForeignKey("contract_assets.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Relationships
    user = relationship("User", backref="documents")
    property = relationship("Property", backref="documents")
    contract = relationship("ContractAsset", backref="documents")
    
    def __repr__(self):
        return f"<Document {self.id}: {self.filename} - {self.document_type}>" 