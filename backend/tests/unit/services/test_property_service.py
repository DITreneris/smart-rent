"""
Unit tests for the PropertyService.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from bson import ObjectId
from fastapi import HTTPException

class TestPropertyService:
    """Test cases for the PropertyService."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database."""
        return Mock()

    @pytest.fixture
    def mock_property_collection(self, mock_db):
        """Create a mock property collection."""
        collection = Mock()
        mock_db.__getitem__.return_value = collection
        return collection

    @pytest.fixture
    def sample_property_data(self):
        """Create sample property data."""
        return {
            "_id": ObjectId(),
            "title": "Modern Apartment",
            "description": "A beautiful modern apartment in the city center",
            "price": 1500.00,
            "location": "City Center",
            "owner_id": ObjectId(),
            "status": "available",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

    def test_create_property(self, mock_property_collection, sample_property_data):
        """Test creating a new property."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        property_data = {
            "title": sample_property_data["title"],
            "description": sample_property_data["description"],
            "price": sample_property_data["price"],
            "location": sample_property_data["location"],
            "owner_id": str(sample_property_data["owner_id"])
        }
        mock_property_collection.insert_one.return_value.inserted_id = sample_property_data["_id"]

        # Act
        result = service.create_property(property_data)

        # Assert
        assert result["_id"] == sample_property_data["_id"]
        assert result["title"] == property_data["title"]
        assert result["status"] == "available"
        mock_property_collection.insert_one.assert_called_once()

    def test_get_property_by_id(self, mock_property_collection, sample_property_data):
        """Test retrieving a property by ID."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        mock_property_collection.find_one.return_value = sample_property_data

        # Act
        result = service.get_property_by_id(str(sample_property_data["_id"]))

        # Assert
        assert result == sample_property_data
        mock_property_collection.find_one.assert_called_once_with(
            {"_id": sample_property_data["_id"]}
        )

    def test_get_property_by_id_not_found(self, mock_property_collection):
        """Test retrieving a non-existent property by ID."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        mock_property_collection.find_one.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.get_property_by_id(str(ObjectId()))
        
        assert exc_info.value.status_code == 404
        assert "Property not found" in str(exc_info.value.detail)

    def test_update_property(self, mock_property_collection, sample_property_data):
        """Test updating a property."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        update_data = {
            "title": "Updated Title",
            "price": 2000.00
        }
        mock_property_collection.find_one_and_update.return_value = {
            **sample_property_data,
            **update_data
        }

        # Act
        result = service.update_property(str(sample_property_data["_id"]), update_data)

        # Assert
        assert result["title"] == update_data["title"]
        assert result["price"] == update_data["price"]
        mock_property_collection.find_one_and_update.assert_called_once()

    def test_delete_property(self, mock_property_collection, sample_property_data):
        """Test deleting a property."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        mock_property_collection.delete_one.return_value.deleted_count = 1

        # Act
        service.delete_property(str(sample_property_data["_id"]))

        # Assert
        mock_property_collection.delete_one.assert_called_once_with(
            {"_id": sample_property_data["_id"]}
        )

    def test_delete_property_not_found(self, mock_property_collection):
        """Test deleting a non-existent property."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        mock_property_collection.delete_one.return_value.deleted_count = 0

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.delete_property(str(ObjectId()))
        
        assert exc_info.value.status_code == 404
        assert "Property not found" in str(exc_info.value.detail)

    def test_list_properties(self, mock_property_collection, sample_property_data):
        """Test listing properties with filters."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        mock_property_collection.find.return_value = [sample_property_data]
        filters = {
            "status": "available",
            "min_price": 1000,
            "max_price": 2000
        }

        # Act
        result = service.list_properties(filters)

        # Assert
        assert len(result) == 1
        assert result[0] == sample_property_data
        mock_property_collection.find.assert_called_once()

    def test_list_properties_empty(self, mock_property_collection):
        """Test listing properties when none match the filters."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        mock_property_collection.find.return_value = []

        # Act
        result = service.list_properties({})

        # Assert
        assert len(result) == 0
        mock_property_collection.find.assert_called_once()

    def test_get_properties_by_owner(self, mock_property_collection, sample_property_data):
        """Test getting properties by owner ID."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        mock_property_collection.find.return_value = [sample_property_data]

        # Act
        result = service.get_properties_by_owner(str(sample_property_data["owner_id"]))

        # Assert
        assert len(result) == 1
        assert result[0] == sample_property_data
        mock_property_collection.find.assert_called_once_with(
            {"owner_id": sample_property_data["owner_id"]}
        )

    def test_update_property_status(self, mock_property_collection, sample_property_data):
        """Test updating a property's status."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        new_status = "rented"
        mock_property_collection.find_one_and_update.return_value = {
            **sample_property_data,
            "status": new_status
        }

        # Act
        result = service.update_property_status(
            str(sample_property_data["_id"]),
            new_status
        )

        # Assert
        assert result["status"] == new_status
        mock_property_collection.find_one_and_update.assert_called_once()

    def test_update_property_status_invalid(self, mock_property_collection, sample_property_data):
        """Test updating a property's status with an invalid status."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        invalid_status = "invalid_status"

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.update_property_status(
                str(sample_property_data["_id"]),
                invalid_status
            )
        
        assert exc_info.value.status_code == 400
        assert "Invalid status" in str(exc_info.value.detail)
        mock_property_collection.find_one_and_update.assert_not_called()

    def test_search_properties(self, mock_property_collection, sample_property_data):
        """Test searching properties by text."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        search_text = "modern"
        mock_property_collection.find.return_value = [sample_property_data]

        # Act
        result = service.search_properties(search_text)

        # Assert
        assert len(result) == 1
        assert result[0] == sample_property_data
        mock_property_collection.find.assert_called_once()

    def test_get_property_statistics(self, mock_property_collection):
        """Test getting property statistics."""
        # Arrange
        from app.services.property_service import PropertyService
        service = PropertyService(mock_property_collection)
        mock_property_collection.count_documents.side_effect = [5, 3, 2]  # total, available, rented

        # Act
        result = service.get_property_statistics()

        # Assert
        assert result["total_properties"] == 5
        assert result["available_properties"] == 3
        assert result["rented_properties"] == 2
        assert mock_property_collection.count_documents.call_count == 3 