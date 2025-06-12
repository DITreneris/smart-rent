"""
MongoDB fixtures for unit testing the SmartRent application.

This module provides fixtures for testing with MongoDB, using 
mongomock for in-memory testing to avoid external dependencies.
"""

import pytest
import mongomock
import motor.motor_asyncio
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Dict, List, Any

@pytest.fixture(scope="function")
def mock_mongodb():
    """
    Create a mock MongoDB instance for unit testing.
    
    Returns:
        mongomock.MongoClient: A mock MongoDB client.
    """
    return mongomock.MongoClient()

@pytest.fixture(scope="function")
def mock_db(mock_mongodb):
    """
    Create a mock database for unit testing.
    
    Args:
        mock_mongodb: The mock MongoDB client fixture.
        
    Returns:
        mongomock.Database: A mock MongoDB database.
    """
    return mock_mongodb["test_db"]

@pytest.fixture(scope="function")
async def mock_motor_client():
    """
    Create a mock AsyncIOMotorClient for unit testing async code.
    
    Returns:
        mongomock.AsyncIOMotorClient: A mock MongoDB async client.
    """
    return mongomock.MongoMotorClient()

@pytest.fixture(scope="function")
async def mock_motor_db(mock_motor_client):
    """
    Create a mock async database for unit testing.
    
    Args:
        mock_motor_client: The mock async MongoDB client fixture.
        
    Returns:
        mongomock.AsyncIOMotorDatabase: A mock async MongoDB database.
    """
    return mock_motor_client["test_db"]

@pytest.fixture(scope="function")
def sample_user_data():
    """
    Generate sample user data for testing.
    
    Returns:
        dict: A dictionary of sample user data.
    """
    return {
        "_id": ObjectId(),
        "email": "test@example.com",
        "hashed_password": "hashed_password_example",
        "full_name": "Test User",
        "is_active": True,
        "role": "tenant",
        "wallet_address": "0x1234567890abcdef1234567890abcdef12345678",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

@pytest.fixture(scope="function")
def sample_landlord_data():
    """
    Generate sample landlord data for testing.
    
    Returns:
        dict: A dictionary of sample landlord data.
    """
    return {
        "_id": ObjectId(),
        "email": "landlord@example.com",
        "hashed_password": "hashed_password_example",
        "full_name": "Test Landlord",
        "is_active": True,
        "role": "landlord",
        "wallet_address": "0xabcdef1234567890abcdef1234567890abcdef12",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

@pytest.fixture(scope="function")
def sample_admin_data():
    """
    Generate sample admin data for testing.
    
    Returns:
        dict: A dictionary of sample admin data.
    """
    return {
        "_id": ObjectId(),
        "email": "admin@example.com",
        "hashed_password": "hashed_password_example",
        "full_name": "Test Admin",
        "is_active": True,
        "role": "admin",
        "wallet_address": "0x7890abcdef1234567890abcdef1234567890abcd",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

@pytest.fixture(scope="function")
def sample_property_data(sample_landlord_data):
    """
    Generate sample property data for testing.
    
    Args:
        sample_landlord_data: The sample landlord data fixture.
        
    Returns:
        dict: A dictionary of sample property data.
    """
    return {
        "_id": ObjectId(),
        "title": "Test Property",
        "description": "A beautiful test property",
        "price": 1000,
        "bedrooms": 2,
        "bathrooms": 1,
        "area": 75,
        "amenities": ["wifi", "parking", "gym"],
        "address": {
            "street": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip": "12345",
            "country": "Testland"
        },
        "blockchain_id": "property_123",
        "metadataURI": "ipfs://property123",
        "status": "available",
        "owner_id": sample_landlord_data["_id"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

@pytest.fixture(scope="function")
def sample_proposal_data(sample_property_data, sample_user_data):
    """
    Generate sample proposal data for testing.
    
    Args:
        sample_property_data: The sample property data fixture.
        sample_user_data: The sample user data fixture.
        
    Returns:
        dict: A dictionary of sample proposal data.
    """
    start_date = datetime.utcnow() + timedelta(days=7)
    end_date = start_date + timedelta(days=365)
    
    return {
        "_id": ObjectId(),
        "property_id": sample_property_data["_id"],
        "tenant_id": sample_user_data["_id"],
        "start_date": start_date,
        "end_date": end_date,
        "offer_amount": 950,
        "status": "pending",
        "terms": {
            "deposit": 950,
            "payment_schedule": "monthly",
            "special_conditions": "No pets allowed"
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

@pytest.fixture(scope="function")
def sample_contract_data(sample_property_data, sample_landlord_data, sample_user_data):
    """
    Generate sample contract data for testing.
    
    Args:
        sample_property_data: The sample property data fixture.
        sample_landlord_data: The sample landlord data fixture.
        sample_user_data: The sample user data fixture.
        
    Returns:
        dict: A dictionary of sample contract data.
    """
    start_date = datetime.utcnow() + timedelta(days=7)
    end_date = start_date + timedelta(days=365)
    
    return {
        "_id": ObjectId(),
        "blockchain_id": "contract_123",
        "property_id": sample_property_data["_id"],
        "landlord_id": sample_landlord_data["_id"],
        "tenant_id": sample_user_data["_id"],
        "start_date": start_date,
        "end_date": end_date,
        "amount": 1000,
        "terms": {
            "deposit": 1000,
            "payment_schedule": "monthly",
            "special_conditions": "No pets allowed"
        },
        "status": "active",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

@pytest.fixture(scope="function")
def sample_document_data(sample_user_data, sample_property_data):
    """
    Generate sample document data for testing.
    
    Args:
        sample_user_data: The sample user data fixture.
        sample_property_data: The sample property data fixture.
        
    Returns:
        dict: A dictionary of sample document data.
    """
    return {
        "_id": ObjectId(),
        "user_id": sample_user_data["_id"],
        "property_id": sample_property_data["_id"],
        "contract_id": None,
        "filename": "test_document.pdf",
        "file_type": "application/pdf",
        "storage_path": "/storage/documents/test_document.pdf",
        "document_type": "ID",
        "uploaded_at": datetime.utcnow()
    }

@pytest.fixture(scope="function")
def populate_mock_db(mock_db, sample_user_data, sample_landlord_data, sample_admin_data, 
                     sample_property_data, sample_proposal_data, sample_contract_data,
                     sample_document_data):
    """
    Populate the mock database with sample data.
    
    Args:
        mock_db: The mock database fixture.
        sample_user_data: The sample user data fixture.
        sample_landlord_data: The sample landlord data fixture.
        sample_admin_data: The sample admin data fixture.
        sample_property_data: The sample property data fixture.
        sample_proposal_data: The sample proposal data fixture.
        sample_contract_data: The sample contract data fixture.
        sample_document_data: The sample document data fixture.
        
    Returns:
        Dict[str, List[Any]]: A dictionary mapping collection names to lists of inserted documents.
    """
    # Create the collections
    users_collection = mock_db["users"]
    properties_collection = mock_db["properties"]
    proposals_collection = mock_db["proposals"]
    contracts_collection = mock_db["contracts"]
    documents_collection = mock_db["documents"]
    
    # Insert the sample data
    users_collection.insert_many([sample_user_data, sample_landlord_data, sample_admin_data])
    properties_collection.insert_one(sample_property_data)
    proposals_collection.insert_one(sample_proposal_data)
    contracts_collection.insert_one(sample_contract_data)
    documents_collection.insert_one(sample_document_data)
    
    # Create indexes
    users_collection.create_index("email", unique=True)
    users_collection.create_index("wallet_address", unique=True, sparse=True)
    properties_collection.create_index("blockchain_id", unique=True, sparse=True)
    properties_collection.create_index("owner_id")
    proposals_collection.create_index("property_id")
    proposals_collection.create_index("tenant_id")
    contracts_collection.create_index("blockchain_id", unique=True, sparse=True)
    contracts_collection.create_index("property_id")
    documents_collection.create_index("user_id")
    documents_collection.create_index("property_id", sparse=True)
    documents_collection.create_index("contract_id", sparse=True)
    
    return {
        "users": [sample_user_data, sample_landlord_data, sample_admin_data],
        "properties": [sample_property_data],
        "proposals": [sample_proposal_data],
        "contracts": [sample_contract_data],
        "documents": [sample_document_data]
    } 