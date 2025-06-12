"""
Unit tests for the Property model.
"""

import pytest
from bson import ObjectId
from datetime import datetime
import mongomock
from pymongo.errors import DuplicateKeyError

class TestPropertyModel:
    """Test cases for the Property model."""

    def test_create_property(self, mock_db, sample_landlord_data):
        """Test that a property can be created with valid data."""
        # Arrange
        properties = mock_db["properties"]
        property_data = {
            "title": "New Test Property",
            "description": "A beautiful new test property",
            "price": 1200,
            "bedrooms": 3,
            "bathrooms": 2,
            "area": 90,
            "amenities": ["wifi", "parking", "gym", "pool"],
            "address": {
                "street": "456 New St",
                "city": "New City",
                "state": "NS",
                "zip": "54321",
                "country": "Testland"
            },
            "blockchain_id": "property_456",
            "metadataURI": "ipfs://property456",
            "status": "available",
            "owner_id": sample_landlord_data["_id"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Act
        result = properties.insert_one(property_data)
        inserted_property = properties.find_one({"_id": result.inserted_id})
        
        # Assert
        assert result.acknowledged
        assert inserted_property["title"] == property_data["title"]
        assert inserted_property["price"] == property_data["price"]
        assert inserted_property["bedrooms"] == property_data["bedrooms"]
        assert inserted_property["owner_id"] == sample_landlord_data["_id"]
        assert inserted_property["status"] == "available"

    def test_find_property_by_id(self, mock_db, populate_mock_db):
        """Test that a property can be found by ID."""
        # Arrange
        properties = mock_db["properties"]
        sample_property = populate_mock_db["properties"][0]
        
        # Act
        found_property = properties.find_one({"_id": sample_property["_id"]})
        
        # Assert
        assert found_property is not None
        assert found_property["_id"] == sample_property["_id"]
        assert found_property["title"] == sample_property["title"]

    def test_find_properties_by_owner(self, mock_db, populate_mock_db):
        """Test that properties can be found by owner."""
        # Arrange
        properties = mock_db["properties"]
        sample_property = populate_mock_db["properties"][0]
        owner_id = sample_property["owner_id"]
        
        # Act
        owner_properties = list(properties.find({"owner_id": owner_id}))
        
        # Assert
        assert len(owner_properties) == 1
        assert owner_properties[0]["_id"] == sample_property["_id"]
        assert owner_properties[0]["owner_id"] == owner_id

    def test_update_property(self, mock_db, populate_mock_db):
        """Test that a property can be updated."""
        # Arrange
        properties = mock_db["properties"]
        sample_property = populate_mock_db["properties"][0]
        new_price = 1500
        new_status = "rented"
        
        # Act
        result = properties.update_one(
            {"_id": sample_property["_id"]},
            {"$set": {
                "price": new_price,
                "status": new_status,
                "updated_at": datetime.utcnow()
            }}
        )
        updated_property = properties.find_one({"_id": sample_property["_id"]})
        
        # Assert
        assert result.modified_count == 1
        assert updated_property["price"] == new_price
        assert updated_property["status"] == new_status
        assert updated_property["title"] == sample_property["title"]  # Other fields remain unchanged

    def test_delete_property(self, mock_db, populate_mock_db):
        """Test that a property can be deleted."""
        # Arrange
        properties = mock_db["properties"]
        sample_property = populate_mock_db["properties"][0]
        initial_count = properties.count_documents({})
        
        # Act
        result = properties.delete_one({"_id": sample_property["_id"]})
        
        # Assert
        assert result.deleted_count == 1
        assert properties.count_documents({}) == initial_count - 1
        assert properties.find_one({"_id": sample_property["_id"]}) is None

    def test_blockchain_id_uniqueness(self, mock_db, populate_mock_db):
        """Test that blockchain_id uniqueness is enforced."""
        # Arrange
        properties = mock_db["properties"]
        sample_property = populate_mock_db["properties"][0]
        sample_landlord = populate_mock_db["users"][1]  # Landlord
        
        duplicate_property = {
            "title": "Duplicate Blockchain ID Property",
            "description": "A property with duplicate blockchain ID",
            "price": 1100,
            "bedrooms": 2,
            "bathrooms": 1,
            "area": 75,
            "blockchain_id": sample_property["blockchain_id"],  # Same blockchain_id
            "status": "available",
            "owner_id": sample_landlord["_id"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Act & Assert
        with pytest.raises(DuplicateKeyError):
            properties.insert_one(duplicate_property)

    def test_find_available_properties(self, mock_db, populate_mock_db):
        """Test that available properties can be found."""
        # Arrange
        properties = mock_db["properties"]
        sample_property = populate_mock_db["properties"][0]
        sample_landlord = populate_mock_db["users"][1]  # Landlord
        
        # Add a rented property
        rented_property = {
            "title": "Rented Property",
            "description": "A property that is already rented",
            "price": 1300,
            "bedrooms": 2,
            "bathrooms": 1,
            "area": 80,
            "status": "rented",
            "owner_id": sample_landlord["_id"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        properties.insert_one(rented_property)
        
        # Act
        available_properties = list(properties.find({"status": "available"}))
        rented_properties = list(properties.find({"status": "rented"}))
        
        # Assert
        assert len(available_properties) == 1
        assert len(rented_properties) == 1
        assert available_properties[0]["_id"] == sample_property["_id"]
        assert available_properties[0]["status"] == "available"
        assert rented_properties[0]["status"] == "rented"

    def test_find_properties_by_price_range(self, mock_db, populate_mock_db):
        """Test that properties can be found by price range."""
        # Arrange
        properties = mock_db["properties"]
        sample_property = populate_mock_db["properties"][0]  # Price 1000
        sample_landlord = populate_mock_db["users"][1]  # Landlord
        
        # Add properties with different prices
        cheap_property = {
            "title": "Cheap Property",
            "description": "An affordable property",
            "price": 500,
            "bedrooms": 1,
            "bathrooms": 1,
            "area": 50,
            "status": "available",
            "owner_id": sample_landlord["_id"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        expensive_property = {
            "title": "Expensive Property",
            "description": "A luxury property",
            "price": 2000,
            "bedrooms": 4,
            "bathrooms": 3,
            "area": 150,
            "status": "available",
            "owner_id": sample_landlord["_id"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        properties.insert_many([cheap_property, expensive_property])
        
        # Act
        low_price_properties = list(properties.find({"price": {"$lte": 750}}))
        mid_price_properties = list(properties.find({"price": {"$gt": 750, "$lt": 1500}}))
        high_price_properties = list(properties.find({"price": {"$gte": 1500}}))
        
        # Assert
        assert len(low_price_properties) == 1
        assert len(mid_price_properties) == 1
        assert len(high_price_properties) == 1
        assert low_price_properties[0]["price"] == 500
        assert mid_price_properties[0]["price"] == 1000
        assert high_price_properties[0]["price"] == 2000

    def test_create_property_with_minimal_fields(self, mock_db, sample_landlord_data):
        """Test that a property can be created with minimal required fields."""
        # Arrange
        properties = mock_db["properties"]
        minimal_property = {
            "title": "Minimal Property",
            "price": 800,
            "owner_id": sample_landlord_data["_id"]
        }
        
        # Act
        result = properties.insert_one(minimal_property)
        inserted_property = properties.find_one({"_id": result.inserted_id})
        
        # Assert
        assert result.acknowledged
        assert inserted_property["title"] == minimal_property["title"]
        assert inserted_property["price"] == minimal_property["price"]
        assert inserted_property["owner_id"] == sample_landlord_data["_id"] 