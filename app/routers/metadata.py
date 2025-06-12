"""
API router for retrieving publicly accessible metadata.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

# Assuming service layer exists
from app.services.rental_metadata import RentalMetadataService

# Assuming dependency injectors exist
from app.api.deps import get_db # Adjust import if needed

router = APIRouter()

# Note: This endpoint is designed to be public (no authentication)
# It mirrors how one might fetch data from IPFS via a gateway.
@router.get("/rentals/{metadata_id}", 
            response_model=Dict[str, Any], 
            summary="Get Public Rental Confirmation Metadata",
            description="Retrieves the publicly accessible JSON metadata associated with a confirmed rental agreement, typically referenced by a URI in a blockchain event.")
def get_rental_metadata(
    metadata_id: str,
    db: Session = Depends(get_db)
):
    """Retrieves the stored JSON metadata for a given metadata ID."""
    metadata_record = RentalMetadataService.get_metadata_by_id(db=db, metadata_id=metadata_id)
    
    if not metadata_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metadata not found")
        
    # Return the raw data dictionary stored in the JSON field
    return metadata_record.data 