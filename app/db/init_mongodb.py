"""
MongoDB initialization script.
Sets up MongoDB collections, indexes, and initial data.
"""

import asyncio
import logging
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.mongo_db import setup_collections

logger = logging.getLogger(__name__)


async def init_mongodb():
    """Initialize MongoDB database with collections and indexes."""
    try:
        logger.info("Initializing MongoDB Atlas connection...")
        
        # Set up collections and indexes
        await setup_collections()
        
        logger.info("MongoDB Atlas initialized successfully.")
    except ServerSelectionTimeoutError as e:
        logger.error(f"Error connecting to MongoDB Atlas: Server selection timed out. {str(e)}")
        logger.error("Please check your network connection and MongoDB Atlas credentials.")
        raise
    except ConnectionFailure as e:
        logger.error(f"Error connecting to MongoDB Atlas: Connection failed. {str(e)}")
        logger.error("Please check your MongoDB Atlas connection string and network settings.")
        raise
    except Exception as e:
        logger.error(f"Error initializing MongoDB Atlas: {str(e)}")
        raise


def init_mongodb_sync():
    """Initialize MongoDB synchronously (for scripts)."""
    try:
        logger.info("Initializing MongoDB Atlas synchronously...")
        
        # Connect to MongoDB with timeout settings
        client = MongoClient(
            settings.MONGO_CONNECTION_STRING,
            server_api=ServerApi('1'),
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=10000,         # 10 second connection timeout
            socketTimeoutMS=30000           # 30 second socket timeout
        )
        
        # Test connection
        client.admin.command('ping')
        logger.info("Pinged MongoDB Atlas deployment. Successfully connected to MongoDB!")
        
        db = client[settings.MONGO_DB_NAME]
        
        # Create indexes for collections
        # Property collection indexes
        db.properties.create_index("blockchain_id", unique=True, sparse=True)
        
        # User collection indexes
        db.users.create_index("email", unique=True)
        db.users.create_index("wallet_address", unique=True, sparse=True)
        
        # Proposal collection indexes
        db.proposals.create_index("property_id")
        db.proposals.create_index("tenant_id")
        
        # Contract collection indexes
        db.contracts.create_index("blockchain_id", unique=True, sparse=True)
        db.contracts.create_index("property_id")
        
        # Photos collection indexes
        db.property_photos.create_index("property_id")
        
        # Document collection indexes
        db.documents.create_index("user_id")
        db.documents.create_index("property_id", sparse=True)
        db.documents.create_index("contract_id", sparse=True)
        
        logger.info("MongoDB Atlas indexes created successfully.")
    except ServerSelectionTimeoutError as e:
        logger.error(f"Error connecting to MongoDB Atlas: Server selection timed out. {str(e)}")
        logger.error("Please check your network connection and MongoDB Atlas credentials.")
        raise
    except ConnectionFailure as e:
        logger.error(f"Error connecting to MongoDB Atlas: Connection failed. {str(e)}")
        logger.error("Please check your MongoDB Atlas connection string and network settings.")
        raise
    except Exception as e:
        logger.error(f"Error initializing MongoDB Atlas synchronously: {str(e)}")
        raise


if __name__ == "__main__":
    # Run MongoDB initialization when script is called directly
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    init_mongodb_sync() 