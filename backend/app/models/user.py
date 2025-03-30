from sqlalchemy import Boolean, Column, String, Enum, DateTime
from sqlalchemy.sql import func
import uuid
from sqlalchemy.orm import relationship

from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum("landlord", "tenant", "admin", name="user_role"), default="tenant")
    wallet_address = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    properties = relationship("Property", back_populates="owner") 