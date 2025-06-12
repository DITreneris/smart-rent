"""
Unit tests for the UserService.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from bson import ObjectId
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

class TestUserService:
    """Test cases for the UserService."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database."""
        return Mock()

    @pytest.fixture
    def mock_user_collection(self, mock_db):
        """Create a mock user collection."""
        collection = Mock()
        mock_db.__getitem__.return_value = collection
        return collection

    @pytest.fixture
    def sample_user_data(self):
        """Create sample user data."""
        return {
            "_id": ObjectId(),
            "email": "test@example.com",
            "wallet_address": "0x1234567890abcdef",
            "role": "tenant",
            "first_name": "John",
            "last_name": "Doe",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

    def test_create_user(self, mock_user_collection, sample_user_data):
        """Test creating a new user."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        user_data = {
            "email": sample_user_data["email"],
            "wallet_address": sample_user_data["wallet_address"],
            "role": sample_user_data["role"],
            "first_name": sample_user_data["first_name"],
            "last_name": sample_user_data["last_name"]
        }
        mock_user_collection.insert_one.return_value.inserted_id = sample_user_data["_id"]

        # Act
        result = service.create_user(user_data)

        # Assert
        assert result["_id"] == sample_user_data["_id"]
        assert result["email"] == user_data["email"]
        assert result["role"] == user_data["role"]
        mock_user_collection.insert_one.assert_called_once()

    def test_create_user_duplicate_email(self, mock_user_collection, sample_user_data):
        """Test creating a user with a duplicate email."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        user_data = {
            "email": sample_user_data["email"],
            "wallet_address": "0x9876543210fedcba",
            "role": "tenant"
        }
        mock_user_collection.insert_one.side_effect = DuplicateKeyError("")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.create_user(user_data)
        
        assert exc_info.value.status_code == 400
        assert "Email already registered" in str(exc_info.value.detail)

    def test_create_user_duplicate_wallet(self, mock_user_collection, sample_user_data):
        """Test creating a user with a duplicate wallet address."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        user_data = {
            "email": "another@example.com",
            "wallet_address": sample_user_data["wallet_address"],
            "role": "tenant"
        }
        mock_user_collection.insert_one.side_effect = DuplicateKeyError("")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.create_user(user_data)
        
        assert exc_info.value.status_code == 400
        assert "Wallet address already registered" in str(exc_info.value.detail)

    def test_get_user_by_id(self, mock_user_collection, sample_user_data):
        """Test retrieving a user by ID."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        mock_user_collection.find_one.return_value = sample_user_data

        # Act
        result = service.get_user_by_id(str(sample_user_data["_id"]))

        # Assert
        assert result == sample_user_data
        mock_user_collection.find_one.assert_called_once_with(
            {"_id": sample_user_data["_id"]}
        )

    def test_get_user_by_id_not_found(self, mock_user_collection):
        """Test retrieving a non-existent user by ID."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        mock_user_collection.find_one.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.get_user_by_id(str(ObjectId()))
        
        assert exc_info.value.status_code == 404
        assert "User not found" in str(exc_info.value.detail)

    def test_get_user_by_email(self, mock_user_collection, sample_user_data):
        """Test retrieving a user by email."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        mock_user_collection.find_one.return_value = sample_user_data

        # Act
        result = service.get_user_by_email(sample_user_data["email"])

        # Assert
        assert result == sample_user_data
        mock_user_collection.find_one.assert_called_once_with(
            {"email": sample_user_data["email"]}
        )

    def test_get_user_by_wallet(self, mock_user_collection, sample_user_data):
        """Test retrieving a user by wallet address."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        mock_user_collection.find_one.return_value = sample_user_data

        # Act
        result = service.get_user_by_wallet(sample_user_data["wallet_address"])

        # Assert
        assert result == sample_user_data
        mock_user_collection.find_one.assert_called_once_with(
            {"wallet_address": sample_user_data["wallet_address"]}
        )

    def test_update_user(self, mock_user_collection, sample_user_data):
        """Test updating a user."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }
        mock_user_collection.find_one_and_update.return_value = {
            **sample_user_data,
            **update_data
        }

        # Act
        result = service.update_user(str(sample_user_data["_id"]), update_data)

        # Assert
        assert result["first_name"] == update_data["first_name"]
        assert result["last_name"] == update_data["last_name"]
        mock_user_collection.find_one_and_update.assert_called_once()

    def test_update_user_not_found(self, mock_user_collection):
        """Test updating a non-existent user."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        mock_user_collection.find_one_and_update.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.update_user(str(ObjectId()), {"first_name": "Updated"})
        
        assert exc_info.value.status_code == 404
        assert "User not found" in str(exc_info.value.detail)

    def test_delete_user(self, mock_user_collection, sample_user_data):
        """Test deleting a user."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        mock_user_collection.delete_one.return_value.deleted_count = 1

        # Act
        service.delete_user(str(sample_user_data["_id"]))

        # Assert
        mock_user_collection.delete_one.assert_called_once_with(
            {"_id": sample_user_data["_id"]}
        )

    def test_delete_user_not_found(self, mock_user_collection):
        """Test deleting a non-existent user."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        mock_user_collection.delete_one.return_value.deleted_count = 0

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.delete_user(str(ObjectId()))
        
        assert exc_info.value.status_code == 404
        assert "User not found" in str(exc_info.value.detail)

    def test_list_users(self, mock_user_collection, sample_user_data):
        """Test listing users with filters."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        mock_user_collection.find.return_value = [sample_user_data]
        filters = {
            "role": "tenant",
            "email": "test@example.com"
        }

        # Act
        result = service.list_users(filters)

        # Assert
        assert len(result) == 1
        assert result[0] == sample_user_data
        mock_user_collection.find.assert_called_once()

    def test_list_users_empty(self, mock_user_collection):
        """Test listing users when none match the filters."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        mock_user_collection.find.return_value = []

        # Act
        result = service.list_users({})

        # Assert
        assert len(result) == 0
        mock_user_collection.find.assert_called_once()

    def test_update_user_role(self, mock_user_collection, sample_user_data):
        """Test updating a user's role."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        new_role = "landlord"
        mock_user_collection.find_one_and_update.return_value = {
            **sample_user_data,
            "role": new_role
        }

        # Act
        result = service.update_user_role(
            str(sample_user_data["_id"]),
            new_role
        )

        # Assert
        assert result["role"] == new_role
        mock_user_collection.find_one_and_update.assert_called_once()

    def test_update_user_role_invalid(self, mock_user_collection, sample_user_data):
        """Test updating a user's role with an invalid role."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        invalid_role = "invalid_role"

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.update_user_role(
                str(sample_user_data["_id"]),
                invalid_role
            )
        
        assert exc_info.value.status_code == 400
        assert "Invalid role" in str(exc_info.value.detail)
        mock_user_collection.find_one_and_update.assert_not_called()

    def test_get_user_statistics(self, mock_user_collection):
        """Test getting user statistics."""
        # Arrange
        from app.services.user_service import UserService
        service = UserService(mock_user_collection)
        mock_user_collection.count_documents.side_effect = [10, 5, 3, 2]  # total, tenants, landlords, admins

        # Act
        result = service.get_user_statistics()

        # Assert
        assert result["total_users"] == 10
        assert result["tenants"] == 5
        assert result["landlords"] == 3
        assert result["admins"] == 2
        assert mock_user_collection.count_documents.call_count == 4 