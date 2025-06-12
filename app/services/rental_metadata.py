"""
Service layer for handling Rental Metadata.
"""

# Use AsyncSession and select
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select

from fastapi import HTTPException, status
from typing import Optional, Dict, Any

from app.models.rental_metadata import RentalMetadata, RentalMetadataCreate

class RentalMetadataService:

    @staticmethod
    async def create_metadata(db: AsyncSession, metadata_in: RentalMetadataCreate) -> RentalMetadata:
        """Stores a new metadata record in the database (Async)."""
        if not metadata_in.data:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Metadata content cannot be empty.")
             
        metadata_db = RentalMetadata(
            data=metadata_in.data
        )
        db.add(metadata_db)
        try:
            await db.commit() # Async commit
            await db.refresh(metadata_db) # Async refresh
        except Exception as e:
            await db.rollback() # Async rollback
            # Log error e
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to store metadata.")
            
        return metadata_db

    @staticmethod
    async def get_metadata_by_id(db: AsyncSession, metadata_id: str) -> Optional[RentalMetadata]:
        """Retrieves a metadata record by its ID (Async)."""
        stmt = select(RentalMetadata).where(RentalMetadata.id == metadata_id)
        result = await db.execute(stmt)
        return result.scalars().first() 