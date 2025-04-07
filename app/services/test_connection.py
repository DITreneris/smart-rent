"""
Simple script to test MongoDB Atlas connection.
"""

import logging
import asyncio
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def test_sync_connection():
    """Test synchronous MongoDB connection."""
    try:
        # Create a MongoDB client with Server API
        client = MongoClient(
            settings.MONGO_CONNECTION_STRING,
            server_api=ServerApi('1'),
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=30000
        )
        
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        logger.info("Pinged your deployment. You successfully connected to MongoDB Atlas!")
        
        # Get database and list collections
        db = client[settings.MONGO_DB_NAME]
        collections = db.list_collection_names()
        logger.info(f"Available collections: {collections}")
        
        return True
    except Exception as e:
        logger.error(f"MongoDB connection error: {e}")
        return False


async def test_async_connection():
    """Test asynchronous MongoDB connection."""
    try:
        # Create an async MongoDB client with Server API
        client = AsyncIOMotorClient(
            settings.MONGO_CONNECTION_STRING,
            server_api=ServerApi('1'),
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=30000
        )
        
        # Get database and list collections
        db = client[settings.MONGO_DB_NAME]
        collections = await db.list_collection_names()
        logger.info(f"Available collections (async): {collections}")
        
        return True
    except Exception as e:
        logger.error(f"MongoDB async connection error: {e}")
        return False


async def main():
    """Run both sync and async connection tests."""
    sync_result = test_sync_connection()
    async_result = await test_async_connection()
    
    if sync_result and async_result:
        logger.info("Both synchronous and asynchronous MongoDB connections are working!")
    else:
        logger.error("MongoDB connection test failed.")


if __name__ == "__main__":
    asyncio.run(main()) 