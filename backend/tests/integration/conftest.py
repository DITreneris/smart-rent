"""
Fixtures for integration tests.
This module contains pytest fixtures that can be used across all integration tests.
"""

import asyncio
import os
import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from app.main import app
from app.config import settings
from app.database import get_database


# Test database name to avoid affecting the dev/prod database
TEST_DATABASE_NAME = "smartrent_test"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_mongodb_client():
    """Create a MongoDB client for testing."""
    # Use the test database, but keep the same connection string
    client = AsyncIOMotorClient(
        settings.MONGODB_URL, 
        serverSelectionTimeoutMS=5000
    )
    
    # Test the connection
    try:
        await client.admin.command('ping')
        print("Connected to MongoDB")
    except ServerSelectionTimeoutError:
        pytest.skip("MongoDB not available")
    
    yield client
    
    # Clean up the test database
    await client.drop_database(TEST_DATABASE_NAME)
    client.close()


@pytest.fixture(scope="session")
async def test_mongodb_database(test_mongodb_client):
    """Create a test database."""
    db = test_mongodb_client[TEST_DATABASE_NAME]
    yield db
    # Database is dropped in the test_mongodb_client fixture cleanup


@pytest.fixture
async def test_client(test_mongodb_database):
    """Create a test client for the FastAPI app."""
    # Override the get_database dependency
    async def override_get_database():
        return test_mongodb_database
    
    app.dependency_overrides[get_database] = override_get_database
    
    with TestClient(app) as client:
        yield client
    
    # Reset dependency overrides
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
async def empty_test_database(test_mongodb_database):
    """Ensure the test database is empty before each test."""
    collections = await test_mongodb_database.list_collection_names()
    for collection in collections:
        await test_mongodb_database[collection].delete_many({})
    return test_mongodb_database


@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User",
        "role": "tenant",
        "wallet_address": "0x1234567890abcdef1234567890abcdef12345678"
    }


@pytest.fixture
def test_property_data():
    """Sample property data for testing."""
    return {
        "title": "Luxury Apartment",
        "description": "A beautiful apartment in the city center",
        "address": {
            "street": "123 Main St",
            "city": "Metropolis",
            "state": "NY",
            "zip_code": "10001",
            "country": "USA"
        },
        "price": 1500.00,
        "property_type": "apartment",
        "bedrooms": 2,
        "bathrooms": 2,
        "size": 1200.00,
        "amenities": ["parking", "gym", "pool"],
        "status": "available"
    }


@pytest.fixture
def test_contract_data():
    """Sample contract data for testing."""
    return {
        "start_date": "2025-01-01T00:00:00",
        "end_date": "2026-01-01T00:00:00",
        "amount": 1500.00,
        "status": "active",
        "terms": {
            "deposit": 1500.00,
            "payment_schedule": "monthly",
            "special_conditions": "No pets allowed"
        }
    }


@pytest.fixture
def test_proposal_data():
    """Sample proposal data for testing."""
    return {
        "start_date": "2025-01-01T00:00:00",
        "end_date": "2026-01-01T00:00:00",
        "offer_amount": 1450.00,
        "status": "pending",
        "terms": {
            "deposit": 1450.00,
            "payment_schedule": "monthly",
            "special_conditions": "Pets allowed with additional deposit"
        }
    }


@pytest.fixture
async def test_user(test_client, test_user_data, empty_test_database):
    """Create a test user and return the user data with ID."""
    response = test_client.post("/api/users", json=test_user_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
async def test_property(test_client, test_property_data, test_user, empty_test_database):
    """Create a test property and return the property data with ID."""
    # Add the owner_id to the property data
    property_data = {**test_property_data, "owner_id": test_user["_id"]}
    
    response = test_client.post(
        "/api/properties", 
        json=property_data,
        headers={"Authorization": f"Bearer {test_user.get('access_token', 'fake_token')}"}
    )
    assert response.status_code == 201
    return response.json() 