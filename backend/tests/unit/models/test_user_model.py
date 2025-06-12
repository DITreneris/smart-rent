"""
Unit tests for the User model.
"""

import pytest
from bson import ObjectId
from datetime import datetime
import mongomock
from pymongo.errors import DuplicateKeyError

class TestUserModel:
    """Test cases for the User model."""

    def test_create_user(self, mock_db):
        """Test that a user can be created with valid data."""
        # Arrange
        users = mock_db["users"]
        user_data = {
            "email": "newuser@example.com",
            "hashed_password": "hashed_password_example",
            "full_name": "New User",
            "is_active": True,
            "role": "tenant",
            "wallet_address": "0x9876543210abcdef9876543210abcdef98765432",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Act
        result = users.insert_one(user_data)
        inserted_user = users.find_one({"_id": result.inserted_id})
        
        # Assert
        assert result.acknowledged
        assert inserted_user["email"] == user_data["email"]
        assert inserted_user["full_name"] == user_data["full_name"]
        assert inserted_user["role"] == user_data["role"]
        assert inserted_user["wallet_address"] == user_data["wallet_address"]

    def test_find_user_by_email(self, mock_db, populate_mock_db):
        """Test that a user can be found by email."""
        # Arrange
        users = mock_db["users"]
        sample_user = populate_mock_db["users"][0]
        
        # Act
        found_user = users.find_one({"email": sample_user["email"]})
        
        # Assert
        assert found_user is not None
        assert found_user["email"] == sample_user["email"]
        assert found_user["_id"] == sample_user["_id"]

    def test_update_user(self, mock_db, populate_mock_db):
        """Test that a user can be updated."""
        # Arrange
        users = mock_db["users"]
        sample_user = populate_mock_db["users"][0]
        new_full_name = "Updated User Name"
        
        # Act
        result = users.update_one(
            {"_id": sample_user["_id"]},
            {"$set": {"full_name": new_full_name, "updated_at": datetime.utcnow()}}
        )
        updated_user = users.find_one({"_id": sample_user["_id"]})
        
        # Assert
        assert result.modified_count == 1
        assert updated_user["full_name"] == new_full_name
        assert updated_user["email"] == sample_user["email"]  # Other fields remain unchanged

    def test_delete_user(self, mock_db, populate_mock_db):
        """Test that a user can be deleted."""
        # Arrange
        users = mock_db["users"]
        sample_user = populate_mock_db["users"][0]
        initial_count = users.count_documents({})
        
        # Act
        result = users.delete_one({"_id": sample_user["_id"]})
        
        # Assert
        assert result.deleted_count == 1
        assert users.count_documents({}) == initial_count - 1
        assert users.find_one({"_id": sample_user["_id"]}) is None

    def test_email_uniqueness(self, mock_db, populate_mock_db):
        """Test that email uniqueness is enforced."""
        # Arrange
        users = mock_db["users"]
        sample_user = populate_mock_db["users"][0]
        duplicate_user = {
            "email": sample_user["email"],  # Same email as existing user
            "hashed_password": "different_password",
            "full_name": "Duplicate User",
            "is_active": True,
            "role": "tenant",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Act & Assert
        with pytest.raises(DuplicateKeyError):
            users.insert_one(duplicate_user)

    def test_wallet_address_uniqueness(self, mock_db, populate_mock_db):
        """Test that wallet address uniqueness is enforced."""
        # Arrange
        users = mock_db["users"]
        sample_user = populate_mock_db["users"][0]
        duplicate_wallet_user = {
            "email": "different@example.com",
            "hashed_password": "different_password",
            "full_name": "Different User",
            "is_active": True,
            "role": "tenant",
            "wallet_address": sample_user["wallet_address"],  # Same wallet address
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Act & Assert
        with pytest.raises(DuplicateKeyError):
            users.insert_one(duplicate_wallet_user)

    def test_find_user_by_wallet(self, mock_db, populate_mock_db):
        """Test that a user can be found by wallet address."""
        # Arrange
        users = mock_db["users"]
        sample_user = populate_mock_db["users"][0]
        
        # Act
        found_user = users.find_one({"wallet_address": sample_user["wallet_address"]})
        
        # Assert
        assert found_user is not None
        assert found_user["wallet_address"] == sample_user["wallet_address"]
        assert found_user["_id"] == sample_user["_id"]

    def test_get_users_by_role(self, mock_db, populate_mock_db):
        """Test that users can be filtered by role."""
        # Arrange
        users = mock_db["users"]
        
        # Act
        landlords = list(users.find({"role": "landlord"}))
        tenants = list(users.find({"role": "tenant"}))
        admins = list(users.find({"role": "admin"}))
        
        # Assert
        assert len(landlords) == 1
        assert len(tenants) == 1
        assert len(admins) == 1
        assert landlords[0]["role"] == "landlord"
        assert tenants[0]["role"] == "tenant"
        assert admins[0]["role"] == "admin"

    def test_create_user_with_minimal_fields(self, mock_db):
        """Test that a user can be created with minimal required fields."""
        # Arrange
        users = mock_db["users"]
        minimal_user = {
            "email": "minimal@example.com",
            "hashed_password": "minimal_password",
            "full_name": "Minimal User"
        }
        
        # Act
        result = users.insert_one(minimal_user)
        inserted_user = users.find_one({"_id": result.inserted_id})
        
        # Assert
        assert result.acknowledged
        assert inserted_user["email"] == minimal_user["email"]
        assert inserted_user["full_name"] == minimal_user["full_name"]
        assert inserted_user["hashed_password"] == minimal_user["hashed_password"] 