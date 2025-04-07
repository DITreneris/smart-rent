"""
Property service for database operations.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from bson import ObjectId
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError

from app.core.mongo_db import (
    get_collection, 
    create_document, 
    get_document, 
    update_document,
    delete_document,
    list_documents,
    format_document_for_response
)
from app.config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)

class PropertyService:
    """Service for property database operations."""
    
    COLLECTION = "properties"
    
    @classmethod
    async def create_property(cls, property_data: Dict[str, Any], owner_id: str) -> str:
        """
        Create a new property listing.
        
        Args:
            property_data: Property data
            owner_id: ID of the property owner
            
        Returns:
            Property ID
        """
        logger.info(f"Creating new property for owner {owner_id}")
        
        # Add metadata
        property_data["owner_id"] = owner_id
        property_data["created_at"] = datetime.utcnow()
        property_data["updated_at"] = None
        
        # Set default status if not provided
        if "status" not in property_data:
            property_data["status"] = "available"
        
        # Set blockchain ID to None if not provided
        if "blockchain_id" not in property_data:
            property_data["blockchain_id"] = None
        
        # Create document in MongoDB
        property_id = await create_document(cls.COLLECTION, property_data)
        
        logger.info(f"Created property with ID {property_id}")
        
        return property_id
    
    @classmethod
    async def get_property(cls, property_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a property by ID.
        
        Args:
            property_id: Property ID
            
        Returns:
            Property data or None if not found
        """
        logger.info(f"Fetching property with ID {property_id}")
        
        return await get_document(cls.COLLECTION, property_id)
    
    @classmethod
    async def get_property_by_blockchain_id(cls, blockchain_id: str) -> Optional[Dict]:
        """Get a property by blockchain ID."""
        collection = await get_collection(cls.COLLECTION)
        document = await collection.find_one({"blockchain_id": blockchain_id})
        return format_document_for_response(document) if document else None
    
    @classmethod
    async def update_property(cls, property_id: str, property_data: Dict[str, Any], owner_id: Optional[str] = None) -> bool:
        """
        Update a property.
        
        Args:
            property_id: Property ID
            property_data: Updated property data
            owner_id: Optional owner ID for verification
            
        Returns:
            True if updated, False otherwise
        """
        logger.info(f"Updating property with ID {property_id}")
        
        # In a real implementation, we would:
        # 1. Verify the owner if owner_id is provided
        # 2. Update the document in MongoDB
        
        # For demonstration, always return True
        return await update_document(cls.COLLECTION, property_id, property_data)
    
    @classmethod
    async def delete_property(cls, property_id: str, owner_id: Optional[str] = None) -> bool:
        """
        Delete a property.
        
        Args:
            property_id: Property ID
            owner_id: Optional owner ID for verification
            
        Returns:
            True if deleted, False otherwise
        """
        logger.info(f"Deleting property with ID {property_id}")
        
        # In a real implementation, we would:
        # 1. Verify the owner if owner_id is provided
        # 2. Delete the document from MongoDB
        
        # For demonstration, always return True
        return await delete_document(cls.COLLECTION, property_id)
    
    @classmethod
    async def list_properties(
        cls, 
        filter_query: Dict = None, 
        skip: int = 0, 
        limit: int = 20,
        sort: List = None
    ) -> List[Dict]:
        """List properties with pagination and filtering."""
        return await list_documents(
            cls.COLLECTION, 
            filter_query=filter_query, 
            skip=skip, 
            limit=limit,
            sort=sort
        )
    
    @classmethod
    async def count_properties(cls, filter_query: Dict = None) -> int:
        """Count properties with optional filtering."""
        collection = await get_collection(cls.COLLECTION)
        
        # Default empty filter
        if filter_query is None:
            filter_query = {}
            
        return await collection.count_documents(filter_query)
    
    @classmethod
    async def add_property_photo(cls, property_id: str, photo_data: Dict) -> str:
        """Add a photo to a property."""
        photo_data["property_id"] = property_id
        photo_id = await create_document("property_photos", photo_data)
        return photo_id
    
    @classmethod
    async def get_property_photos(cls, property_id: str) -> List[Dict]:
        """Get photos for a property."""
        return await list_documents(
            "property_photos",
            filter_query={"property_id": property_id},
            limit=50
        )
    
    @classmethod
    async def update_property_blockchain_id(cls, property_id: str, blockchain_id: str) -> bool:
        """
        Update property blockchain ID.
        
        Args:
            property_id: Property ID
            blockchain_id: Blockchain ID
            
        Returns:
            True if updated, False otherwise
        """
        logger.info(f"Updating blockchain ID for property {property_id}: {blockchain_id}")
        
        # In a real implementation, we would update the document in MongoDB
        # For demonstration, always return True
        return await update_document(
            cls.COLLECTION,
            property_id,
            {"blockchain_id": blockchain_id}
        )
    
    @classmethod
    async def get_properties_by_owner(cls, owner_id: str) -> List[Dict[str, Any]]:
        """
        Get properties by owner.
        
        Args:
            owner_id: Owner ID
            
        Returns:
            List of properties
        """
        logger.info(f"Fetching properties for owner {owner_id}")
        
        # In a real implementation, we would query MongoDB
        # For demonstration, we'll return mock data
        return await list_documents(
            cls.COLLECTION,
            filter_query={"owner_id": owner_id},
            sort=[("created_at", -1)]
        )
    
    @classmethod
    async def search_properties(
        cls, 
        filters: Dict[str, Any] = None, 
        sort_by: str = "created_at", 
        sort_order: int = DESCENDING,
        page: int = 1, 
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        Search properties with filters and pagination.
        
        Args:
            filters: Search filters
            sort_by: Field to sort by
            sort_order: Sort order (1 for ascending, -1 for descending)
            page: Page number
            page_size: Items per page
            
        Returns:
            Dictionary with items, total, page, page_size, and pages
        """
        logger.info(f"Searching properties with filters: {filters}")
        
        # In a real implementation, we would query MongoDB
        # For demonstration, we'll return mock data
        mock_properties = [
            {
                "id": f"mock-property-{i}",
                "owner_id": "mock-owner-id",
                "title": f"Property {i}",
                "description": f"Description for property {i}",
                "property_type": "apartment",
                "price_per_month": 1000 + i * 100,
                "security_deposit": 1500 + i * 150,
                "bedrooms": 1 + (i % 3),
                "bathrooms": 1.0 + (i % 2) * 0.5,
                "size_sqm": 50 + i * 10,
                "location": {
                    "address": f"{123 + i} Main St",
                    "city": "New York",
                    "state": "NY",
                    "country": "USA",
                    "postal_code": "10001",
                    "latitude": 40.7128,
                    "longitude": -74.0060
                },
                "amenities": [
                    {
                        "name": "Parking",
                        "description": "Underground parking available",
                        "icon": "parking-icon"
                    }
                ],
                "images": [
                    {
                        "url": f"https://example.com/image{i}.jpg",
                        "description": "Primary image",
                        "is_primary": True,
                        "upload_date": "2025-01-01T00:00:00Z"
                    }
                ],
                "available_from": "2025-05-01T00:00:00Z",
                "minimum_rental_period": 6,
                "maximum_rental_period": 12,
                "status": "available",
                "blockchain_id": None,
                "created_at": "2025-04-01T00:00:00Z",
                "updated_at": None
            }
            for i in range(1, 21)  # 20 mock properties
        ]
        
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_properties = mock_properties[start_idx:end_idx]
        
        total = len(mock_properties)
        pages = (total + page_size - 1) // page_size
        
        return {
            "items": paginated_properties,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages
        } 