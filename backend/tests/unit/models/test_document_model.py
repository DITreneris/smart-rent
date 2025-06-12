"""
Unit tests for the Document model.
"""

import pytest
from bson import ObjectId
from datetime import datetime
import mongomock
from pymongo.errors import DuplicateKeyError

class TestDocumentModel:
    """Test cases for the Document model."""

    def test_create_document(self, mock_db, sample_user_data, sample_property_data):
        """Test that a document can be created with valid data."""
        # Arrange
        documents = mock_db["documents"]
        document_data = {
            "user_id": sample_user_data["_id"],
            "property_id": sample_property_data["_id"],
            "contract_id": None,
            "filename": "lease_agreement.pdf",
            "file_type": "application/pdf",
            "storage_path": "/storage/documents/lease_agreement.pdf",
            "document_type": "lease",
            "uploaded_at": datetime.utcnow()
        }
        
        # Act
        result = documents.insert_one(document_data)
        inserted_document = documents.find_one({"_id": result.inserted_id})
        
        # Assert
        assert result.acknowledged
        assert inserted_document["user_id"] == sample_user_data["_id"]
        assert inserted_document["property_id"] == sample_property_data["_id"]
        assert inserted_document["filename"] == "lease_agreement.pdf"
        assert inserted_document["document_type"] == "lease"

    def test_find_document_by_id(self, mock_db, populate_mock_db):
        """Test that a document can be found by ID."""
        # Arrange
        documents = mock_db["documents"]
        sample_document = populate_mock_db["documents"][0]
        
        # Act
        found_document = documents.find_one({"_id": sample_document["_id"]})
        
        # Assert
        assert found_document is not None
        assert found_document["_id"] == sample_document["_id"]
        assert found_document["filename"] == sample_document["filename"]

    def test_find_documents_by_user(self, mock_db, populate_mock_db):
        """Test that documents can be found by user."""
        # Arrange
        documents = mock_db["documents"]
        sample_document = populate_mock_db["documents"][0]
        user_id = sample_document["user_id"]
        
        # Act
        user_documents = list(documents.find({"user_id": user_id}))
        
        # Assert
        assert len(user_documents) == 1
        assert user_documents[0]["_id"] == sample_document["_id"]
        assert user_documents[0]["user_id"] == user_id

    def test_find_documents_by_property(self, mock_db, populate_mock_db):
        """Test that documents can be found by property."""
        # Arrange
        documents = mock_db["documents"]
        sample_document = populate_mock_db["documents"][0]
        property_id = sample_document["property_id"]
        
        # Act
        property_documents = list(documents.find({"property_id": property_id}))
        
        # Assert
        assert len(property_documents) == 1
        assert property_documents[0]["_id"] == sample_document["_id"]
        assert property_documents[0]["property_id"] == property_id

    def test_find_documents_by_contract(self, mock_db, populate_mock_db, sample_contract_data):
        """Test that documents can be found by contract."""
        # Arrange
        documents = mock_db["documents"]
        sample_document = populate_mock_db["documents"][0]
        
        # Update the sample document to have a contract ID
        documents.update_one(
            {"_id": sample_document["_id"]},
            {"$set": {"contract_id": sample_contract_data["_id"]}}
        )
        
        # Act
        contract_documents = list(documents.find({"contract_id": sample_contract_data["_id"]}))
        
        # Assert
        assert len(contract_documents) == 1
        assert contract_documents[0]["_id"] == sample_document["_id"]
        assert contract_documents[0]["contract_id"] == sample_contract_data["_id"]

    def test_update_document_type(self, mock_db, populate_mock_db):
        """Test that a document's type can be updated."""
        # Arrange
        documents = mock_db["documents"]
        sample_document = populate_mock_db["documents"][0]
        new_document_type = "identification"
        
        # Act
        result = documents.update_one(
            {"_id": sample_document["_id"]},
            {"$set": {
                "document_type": new_document_type
            }}
        )
        updated_document = documents.find_one({"_id": sample_document["_id"]})
        
        # Assert
        assert result.modified_count == 1
        assert updated_document["document_type"] == new_document_type
        assert updated_document["filename"] == sample_document["filename"]  # Other fields remain unchanged

    def test_update_storage_path(self, mock_db, populate_mock_db):
        """Test that a document's storage path can be updated."""
        # Arrange
        documents = mock_db["documents"]
        sample_document = populate_mock_db["documents"][0]
        new_storage_path = "/storage/documents/relocated_file.pdf"
        
        # Act
        result = documents.update_one(
            {"_id": sample_document["_id"]},
            {"$set": {
                "storage_path": new_storage_path
            }}
        )
        updated_document = documents.find_one({"_id": sample_document["_id"]})
        
        # Assert
        assert result.modified_count == 1
        assert updated_document["storage_path"] == new_storage_path
        assert updated_document["filename"] == sample_document["filename"]  # Other fields remain unchanged

    def test_delete_document(self, mock_db, populate_mock_db):
        """Test that a document can be deleted."""
        # Arrange
        documents = mock_db["documents"]
        sample_document = populate_mock_db["documents"][0]
        initial_count = documents.count_documents({})
        
        # Act
        result = documents.delete_one({"_id": sample_document["_id"]})
        
        # Assert
        assert result.deleted_count == 1
        assert documents.count_documents({}) == initial_count - 1
        assert documents.find_one({"_id": sample_document["_id"]}) is None

    def test_find_documents_by_type(self, mock_db, populate_mock_db, sample_user_data):
        """Test that documents can be filtered by type."""
        # Arrange
        documents = mock_db["documents"]
        sample_document = populate_mock_db["documents"][0]  # This one is "ID" type
        
        # Add another document with a different type
        contract_document = {
            "user_id": sample_user_data["_id"],
            "property_id": None,
            "contract_id": None,
            "filename": "rental_agreement.pdf",
            "file_type": "application/pdf",
            "storage_path": "/storage/documents/rental_agreement.pdf",
            "document_type": "contract",
            "uploaded_at": datetime.utcnow()
        }
        documents.insert_one(contract_document)
        
        # Act
        id_documents = list(documents.find({"document_type": "ID"}))
        contract_documents = list(documents.find({"document_type": "contract"}))
        
        # Assert
        assert len(id_documents) == 1
        assert len(contract_documents) == 1
        assert id_documents[0]["document_type"] == "ID"
        assert contract_documents[0]["document_type"] == "contract"

    def test_document_with_minimal_fields(self, mock_db, sample_user_data):
        """Test that a document can be created with minimal required fields."""
        # Arrange
        documents = mock_db["documents"]
        minimal_document = {
            "user_id": sample_user_data["_id"],
            "filename": "minimal_doc.pdf",
            "file_type": "application/pdf",
            "storage_path": "/storage/documents/minimal_doc.pdf",
            "document_type": "other",
            "uploaded_at": datetime.utcnow()
        }
        
        # Act
        result = documents.insert_one(minimal_document)
        inserted_document = documents.find_one({"_id": result.inserted_id})
        
        # Assert
        assert result.acknowledged
        assert inserted_document["user_id"] == sample_user_data["_id"]
        assert inserted_document["filename"] == "minimal_doc.pdf"
        assert inserted_document["document_type"] == "other"
        assert inserted_document["property_id"] is None  # Not provided
        assert inserted_document["contract_id"] is None  # Not provided

    def test_multiple_documents_per_user(self, mock_db, populate_mock_db, sample_user_data):
        """Test that a user can have multiple documents."""
        # Arrange
        documents = mock_db["documents"]
        sample_document = populate_mock_db["documents"][0]
        user_id = sample_document["user_id"]
        
        # Add another document for the same user
        second_document = {
            "user_id": user_id,
            "property_id": None,
            "contract_id": None,
            "filename": "passport.jpg",
            "file_type": "image/jpeg",
            "storage_path": "/storage/documents/passport.jpg",
            "document_type": "identification",
            "uploaded_at": datetime.utcnow()
        }
        documents.insert_one(second_document)
        
        # Act
        user_documents = list(documents.find({"user_id": user_id}))
        
        # Assert
        assert len(user_documents) == 2
        assert any(d["filename"] == sample_document["filename"] for d in user_documents)
        assert any(d["filename"] == "passport.jpg" for d in user_documents)

    def test_search_documents_by_filename(self, mock_db, populate_mock_db):
        """Test that documents can be searched by filename."""
        # Arrange
        documents = mock_db["documents"]
        sample_document = populate_mock_db["documents"][0]
        filename_pattern = sample_document["filename"].split(".")[0]  # Get the part before extension
        
        # Act
        # Using regex to find documents with filenames containing the pattern
        search_results = list(documents.find({"filename": {"$regex": filename_pattern, "$options": "i"}}))
        
        # Assert
        assert len(search_results) == 1
        assert search_results[0]["_id"] == sample_document["_id"]
        assert filename_pattern in search_results[0]["filename"] 