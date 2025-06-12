"""
Model and Schemas for storing Rental Confirmation Metadata.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from sqlalchemy import Column, String, JSON, DateTime
from pydantic import BaseModel, Field

from app.db.base import Base # Assuming Base is correctly defined here


# --- SQLAlchemy Model --- 

class RentalMetadata(Base):
    """SQLAlchemy model for storing rental metadata JSON blobs."""
    
    __tablename__ = "rental_metadata"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # Store the actual metadata dictionary generated in ProposalService
    data = Column(JSON, nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)
    # Optional: Link back to proposal if needed for internal tracking?
    # proposal_id = Column(String(36), ForeignKey("proposals.id"), nullable=True, index=True)

    def __repr__(self):
        return f"<RentalMetadata {self.id}>"

# --- Pydantic Schemas --- 

class RentalMetadataBase(BaseModel):
    """Base schema for rental metadata."""
    data: Dict[str, Any]

    class Config:
        orm_mode = True

class RentalMetadataCreate(RentalMetadataBase):
    """Schema used when creating metadata (input to service)."""
    pass

class RentalMetadataResponse(BaseModel):
    """Schema for returning metadata (the raw data dict)."""
    # We typically just want to return the raw JSON data publicly
    # The API endpoint will fetch the record and return record.data
    # Define this if needed, but often the endpoint returns Dict[str, Any]
    pass 

class RentalMetadataDB(RentalMetadataBase):
     """Schema representing the DB model (including id)."""
     id: str
     created_at: datetime 