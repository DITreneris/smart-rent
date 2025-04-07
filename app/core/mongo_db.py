"""
MongoDB connection utilities for off-chain data storage
"""

import motor.motor_asyncio
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from typing import Dict, Any, List, Optional
from bson import ObjectId
import json
from datetime import datetime
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Connection options
connection_options = {
    "serverSelectionTimeoutMS": 5000,    # 5 seconds for server selection
    "connectTimeoutMS": 10000,           # 10 seconds to establish a connection
    "socketTimeoutMS": 30000,            # 30 seconds for socket operations
    "maxPoolSize": 100,                  # Maximum connection pool size
    "minPoolSize": 10,                   # Minimum connection pool size
    "maxIdleTimeMS": 45000,              # Max time a connection can be idle (45 sec)
    "retryWrites": True,                 # Retry write operations
    "w": "majority"                      # Write concern
}

# Create MongoDB connection string from settings
MONGO_CONNECTION_STRING = settings.MONGO_CONNECTION_STRING

try:
    # MongoDB async client (for FastAPI)
    async_client = motor.motor_asyncio.AsyncIOMotorClient(
        MONGO_CONNECTION_STRING, 
        server_api=ServerApi('1'),
        **connection_options
    )
    db = async_client[settings.MONGO_DB_NAME]
    
    # MongoDB sync client (for migrations and scripts)
    sync_client = MongoClient(
        MONGO_CONNECTION_STRING, 
        server_api=ServerApi('1'),
        **connection_options
    )
    sync_db = sync_client[settings.MONGO_DB_NAME]
    
    # Test connection
    sync_client.admin.command('ping')
    logger.info("Pinged MongoDB Atlas deployment. Successfully connected to MongoDB!")
    
except ServerSelectionTimeoutError:
    logger.error("Failed to connect to MongoDB Atlas: Server selection timeout")
    # We don't want to crash the app during import, just log the error
    # The actual connection will be tested during initialization
    
except ConnectionFailure:
    logger.error("Failed to connect to MongoDB Atlas: Connection failure")
    # We don't want to crash the app during import, just log the error
    
except Exception as e:
    logger.error(f"Failed to connect to MongoDB Atlas: {str(e)}")
    # We don't want to crash the app during import, just log the error


class PyObjectId(ObjectId):
    """Custom ObjectId class for Pydantic models with MongoDB."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


async def get_collection(collection_name: str):
    """Get a collection from the database."""
    return db[collection_name]


def json_serialize_mongodb(obj: Any) -> Any:
    """Custom JSON serializer for MongoDB objects."""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


def format_document_for_response(document: Dict) -> Dict:
    """Format a MongoDB document for API response."""
    if document is None:
        return None
    
    # Convert _id to id
    if "_id" in document:
        document["id"] = str(document["_id"])
        del document["_id"]
    
    # Handle nested documents
    for key, value in document.items():
        if isinstance(value, dict):
            document[key] = format_document_for_response(value)
        elif isinstance(value, list):
            document[key] = [
                format_document_for_response(item) if isinstance(item, dict) else item
                for item in value
            ]
    
    return document


# Common database operations for collections

async def create_document(collection_name: str, document: Dict) -> str:
    """Create a new document in a collection."""
    collection = await get_collection(collection_name)
    
    # Add timestamps
    document["created_at"] = datetime.utcnow()
    document["updated_at"] = datetime.utcnow()
    
    result = await collection.insert_one(document)
    return str(result.inserted_id)


async def get_document(collection_name: str, document_id: str) -> Optional[Dict]:
    """Get a document by ID."""
    collection = await get_collection(collection_name)
    document = await collection.find_one({"_id": ObjectId(document_id)})
    return format_document_for_response(document) if document else None


async def update_document(collection_name: str, document_id: str, update_data: Dict) -> bool:
    """Update a document by ID."""
    collection = await get_collection(collection_name)
    
    # Add updated timestamp
    update_data["updated_at"] = datetime.utcnow()
    
    result = await collection.update_one(
        {"_id": ObjectId(document_id)}, 
        {"$set": update_data}
    )
    return result.modified_count > 0


async def delete_document(collection_name: str, document_id: str) -> bool:
    """Delete a document by ID."""
    collection = await get_collection(collection_name)
    result = await collection.delete_one({"_id": ObjectId(document_id)})
    return result.deleted_count > 0


async def list_documents(
    collection_name: str, 
    filter_query: Dict = None, 
    skip: int = 0, 
    limit: int = 100,
    sort: List = None
) -> List[Dict]:
    """List documents with pagination and filtering."""
    collection = await get_collection(collection_name)
    
    # Default empty filter
    if filter_query is None:
        filter_query = {}
    
    # Execute query with pagination
    cursor = collection.find(filter_query).skip(skip).limit(limit)
    
    # Apply sorting if provided
    if sort:
        cursor = cursor.sort(sort)
    
    # Get and format results
    documents = await cursor.to_list(length=limit)
    return [format_document_for_response(doc) for doc in documents]


# Helper functions for GridFS (file storage)
async def setup_collections():
    """Set up MongoDB collections with initial indexes."""
    try:
        logger.info("Setting up MongoDB collections and indexes...")
        
        # Property collection indexes
        await db.properties.create_index("blockchain_id", unique=True, sparse=True)
        
        # User collection indexes
        await db.users.create_index("email", unique=True)
        await db.users.create_index("wallet_address", unique=True, sparse=True)
        
        # Proposal collection indexes
        await db.proposals.create_index("property_id")
        await db.proposals.create_index("tenant_id")
        
        # Contract collection indexes
        await db.contracts.create_index("blockchain_id", unique=True, sparse=True)
        await db.contracts.create_index("property_id")
        
        # Photos collection indexes
        await db.property_photos.create_index("property_id")
        
        # Document collection indexes
        await db.documents.create_index("user_id")
        await db.documents.create_index("property_id", sparse=True)
        await db.documents.create_index("contract_id", sparse=True)
        
        logger.info("MongoDB collections and indexes set up successfully.")
    except Exception as e:
        logger.error(f"Error setting up MongoDB collections: {str(e)}")
        raise 