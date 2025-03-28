from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, JSON, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class UserRole(str, enum.Enum):
    TENANT = "tenant"
    LANDLORD = "landlord"
    ADMIN = "admin"

class UserStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(Enum(UserRole))
    status = Column(Enum(UserStatus), default=UserStatus.PENDING)
    wallet_address = Column(String, unique=True, nullable=True)
    documents = Column(JSON, nullable=True)  # Store document URLs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    properties = relationship("Property", back_populates="owner")
    contracts_as_tenant = relationship("Contract", back_populates="tenant", foreign_keys="Contract.tenant_id")
    contracts_as_landlord = relationship("Contract", back_populates="landlord", foreign_keys="Contract.landlord_id")
    blockchain_references = relationship("BlockchainReference", back_populates="user")

class PropertyStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    RENTED = "rented"
    UNAVAILABLE = "unavailable"

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    zip_code = Column(String)
    price = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    area = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(PropertyStatus), default=PropertyStatus.PENDING)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="properties")
    contracts = relationship("Contract", back_populates="property")

class ContractStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    tenant_id = Column(Integer, ForeignKey("users.id"))
    landlord_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    monthly_rent = Column(Integer)
    security_deposit = Column(Integer)
    status = Column(Enum(ContractStatus), default=ContractStatus.PENDING)
    contract_address = Column(String, unique=True, nullable=True)  # Ethereum contract address
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    blockchain_tx_hash = Column(String, nullable=True)
    blockchain_agreement_id = Column(Integer, nullable=True)

    # Relationships
    property = relationship("Property", back_populates="contracts")
    tenant = relationship("User", foreign_keys=[tenant_id], back_populates="contracts_as_tenant")
    landlord = relationship("User", foreign_keys=[landlord_id], back_populates="contracts_as_landlord")

class BlockchainReference(Base):
    __tablename__ = "blockchain_references"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_hash = Column(String, unique=True, index=True)
    agreement_id = Column(Integer, nullable=True)
    property_id = Column(String, nullable=True)
    block_number = Column(Integer, nullable=True)
    transaction_type = Column(String, nullable=True)
    status = Column(String, default="confirmed")
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="blockchain_references") 