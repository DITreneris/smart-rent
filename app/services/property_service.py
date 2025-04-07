"""
Property service for database operations.
"""

from typing import Dict, List, Optional, Any, Union
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
from app.models.property import (
    PropertyCreate, 
    PropertyUpdate, 
    PropertyDB, 
    PropertyResponse,
    PropertySearchParams,
    PropertyStatus
)

# Configure logging
logger = logging.getLogger(__name__)

class PropertyService:
    """Service for property database operations."""
    
    COLLECTION = "properties"
    
    @classmethod
    async def create_property(cls, property_data: PropertyCreate, owner_id: str) -> PropertyDB:
        """
        Create a new property listing.
        
        Args:
            property_data: Property data
            owner_id: ID of the property owner
            
        Returns:
            Created property
        """
        logger.info(f"Creating new property for owner {owner_id}")
        
        # Add metadata
        property_data.owner_id = owner_id
        property_data.created_at = datetime.utcnow()
        property_data.updated_at = None
        
        # Set default status if not provided
        if "status" not in property_data:
            property_data.status = "available"
        
        # Set blockchain ID to None if not provided
        if "blockchain_id" not in property_data:
            property_data.blockchain_id = None
        
        # Create document in MongoDB
        property_id = await create_document(cls.COLLECTION, property_data.dict())
        
        logger.info(f"Created property with ID {property_id}")
        
        return PropertyDB(**property_data.dict(), id=property_id)
    
    @classmethod
    async def get_property(cls, property_id: str) -> Optional[PropertyDB]:
        """
        Get a property by ID.
        
        Args:
            property_id: Property ID
            
        Returns:
            Property data or None if not found
        """
        logger.info(f"Fetching property with ID {property_id}")
        
        # Mock property database
        properties = {
            "1": PropertyDB(
                id="1",
                title="Luxury Downtown Apartment",
                description="Beautiful apartment in the heart of downtown",
                property_type="apartment",
                bedrooms=2,
                bathrooms=2.0,
                area=1200.0,
                price=2500.0,
                owner_id="2",  # Landlord user
                address={
                    "street": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "zip_code": "10001",
                    "country": "USA"
                },
                created_at=datetime(2025, 1, 1),
                status="available"
            ),
            "2": PropertyDB(
                id="2",
                title="Cozy Studio Near Park",
                description="Perfect studio apartment near Central Park",
                property_type="apartment",
                bedrooms=0,
                bathrooms=1.0,
                area=500.0,
                price=1500.0,
                owner_id="2",  # Landlord user
                address={
                    "street": "456 Park Ave",
                    "city": "New York",
                    "state": "NY",
                    "zip_code": "10002",
                    "country": "USA"
                },
                created_at=datetime(2025, 1, 2),
                status="available"
            ),
            "3": PropertyDB(
                id="3",
                title="Spacious Family Home",
                description="Large family home with backyard",
                property_type="house",
                bedrooms=4,
                bathrooms=3.5,
                area=2500.0,
                price=3500.0,
                owner_id="2",  # Landlord user
                address={
                    "street": "789 Suburb Dr",
                    "city": "Chicago",
                    "state": "IL",
                    "zip_code": "60007",
                    "country": "USA"
                },
                created_at=datetime(2025, 1, 3),
                status="available"
            )
        }
        
        return properties.get(property_id)
    
    @classmethod
    async def get_property_by_blockchain_id(cls, blockchain_id: str) -> Optional[Dict]:
        """Get a property by blockchain ID."""
        collection = await get_collection(cls.COLLECTION)
        document = await collection.find_one({"blockchain_id": blockchain_id})
        return format_document_for_response(document) if document else None
    
    @classmethod
    async def update_property(cls, property_id: str, property_data: PropertyUpdate, owner_id: str) -> Optional[PropertyDB]:
        """
        Update a property.
        
        Args:
            property_id: Property ID
            property_data: Updated property data
            owner_id: Owner user ID for verification
            
        Returns:
            Updated property or None if not found or not owned by user
        """
        logger.info(f"Updating property with ID {property_id}")
        
        # Get existing property
        existing_property = await cls.get_property(property_id)
        if not existing_property:
            return None
            
        # Verify ownership
        if existing_property.owner_id != owner_id:
            logger.warning(f"User {owner_id} attempted to update property {property_id} owned by {existing_property.owner_id}")
            return None
            
        # Create a dict with only non-None values
        update_data = {k: v for k, v in property_data.dict().items() if v is not None}
        
        # Update the property
        updated_property = PropertyDB(
            **{**existing_property.dict(), **update_data},
            updated_at=datetime.utcnow()
        )
        
        logger.info(f"Updated property: {property_id}")
        
        return updated_property
    
    @classmethod
    async def delete_property(cls, property_id: str, owner_id: str) -> bool:
        """
        Delete a property.
        
        Args:
            property_id: Property ID
            owner_id: Owner user ID for verification
            
        Returns:
            True if deleted, False otherwise
        """
        logger.info(f"Deleting property with ID {property_id}")
        
        # Get existing property
        existing_property = await cls.get_property(property_id)
        if not existing_property:
            return False
            
        # Verify ownership
        if existing_property.owner_id != owner_id:
            logger.warning(f"User {owner_id} attempted to delete property {property_id} owned by {existing_property.owner_id}")
            return False
            
        # Delete the document from MongoDB
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
    async def get_properties_by_owner(cls, owner_id: str) -> List[PropertyDB]:
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
        search_params: PropertySearchParams, 
        limit: int = 10, 
        offset: int = 0
    ) -> List[PropertyDB]:
        """
        Search properties with filters and pagination.
        
        Args:
            search_params: Search parameters
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            List of properties matching search criteria
        """
        logger.info(f"Searching properties with filters: {search_params}")
        
        # In a real implementation, we would query MongoDB
        # For demonstration, we'll return mock data
        properties = [
            PropertyDB(
                id="1",
                title="Luxury Downtown Apartment",
                description="Beautiful apartment in the heart of downtown",
                property_type="apartment",
                bedrooms=2,
                bathrooms=2.0,
                area=1200.0,
                price=2500.0,
                owner_id="2",
                address={
                    "street": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "zip_code": "10001",
                    "country": "USA"
                },
                created_at=datetime(2025, 1, 1),
                status="available"
            ),
            PropertyDB(
                id="2",
                title="Cozy Studio Near Park",
                description="Perfect studio apartment near Central Park",
                property_type="apartment",
                bedrooms=0,
                bathrooms=1.0,
                area=500.0,
                price=1500.0,
                owner_id="2",
                address={
                    "street": "456 Park Ave",
                    "city": "New York",
                    "state": "NY",
                    "zip_code": "10002",
                    "country": "USA"
                },
                created_at=datetime(2025, 1, 2),
                status="available"
            ),
            PropertyDB(
                id="3",
                title="Spacious Family Home",
                description="Large family home with backyard",
                property_type="house",
                bedrooms=4,
                bathrooms=3.5,
                area=2500.0,
                price=3500.0,
                owner_id="2",
                address={
                    "street": "789 Suburb Dr",
                    "city": "Chicago",
                    "state": "IL",
                    "zip_code": "60007",
                    "country": "USA"
                },
                created_at=datetime(2025, 1, 3),
                status="available"
            )
        ]
        
        # Apply filters
        filtered_properties = properties
        
        # Filter by property type
        if search_params.property_type:
            filtered_properties = [p for p in filtered_properties if p.property_type == search_params.property_type]
            
        # Filter by price range
        if search_params.min_price is not None:
            filtered_properties = [p for p in filtered_properties if p.price >= search_params.min_price]
        if search_params.max_price is not None:
            filtered_properties = [p for p in filtered_properties if p.price <= search_params.max_price]
            
        # Filter by bedrooms
        if search_params.min_bedrooms is not None:
            filtered_properties = [p for p in filtered_properties if p.bedrooms >= search_params.min_bedrooms]
        if search_params.max_bedrooms is not None:
            filtered_properties = [p for p in filtered_properties if p.bedrooms <= search_params.max_bedrooms]
            
        # Filter by bathrooms
        if search_params.min_bathrooms is not None:
            filtered_properties = [p for p in filtered_properties if p.bathrooms >= search_params.min_bathrooms]
        if search_params.max_bathrooms is not None:
            filtered_properties = [p for p in filtered_properties if p.bathrooms <= search_params.max_bathrooms]
            
        # Filter by area
        if search_params.min_area is not None:
            filtered_properties = [p for p in filtered_properties if p.area >= search_params.min_area]
        if search_params.max_area is not None:
            filtered_properties = [p for p in filtered_properties if p.area <= search_params.max_area]
            
        # Filter by location
        if search_params.city:
            filtered_properties = [p for p in filtered_properties if p.address.city.lower() == search_params.city.lower()]
        if search_params.state:
            filtered_properties = [p for p in filtered_properties if p.address.state.lower() == search_params.state.lower()]
        if search_params.country:
            filtered_properties = [p for p in filtered_properties if p.address.country.lower() == search_params.country.lower()]
            
        # Filter by amenities
        if search_params.is_furnished is not None:
            filtered_properties = [p for p in filtered_properties if p.is_furnished == search_params.is_furnished]
        if search_params.pets_allowed is not None:
            filtered_properties = [p for p in filtered_properties if p.pets_allowed == search_params.pets_allowed]
        if search_params.utilities_included is not None:
            filtered_properties = [p for p in filtered_properties if p.utilities_included == search_params.utilities_included]
            
        # Filter by status
        if search_params.status:
            filtered_properties = [p for p in filtered_properties if p.status == search_params.status]
            
        # Apply pagination
        paginated_properties = filtered_properties[offset:offset + limit]
        
        return paginated_properties 