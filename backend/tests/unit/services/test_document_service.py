"""
Unit tests for the DocumentService.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from bson import ObjectId
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

class TestDocumentService:
    """Test cases for the DocumentService."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database."""
        return Mock()

    @pytest.fixture
    def mock_document_collection(self, mock_db):
        """Create a mock document collection."""
        collection = Mock()
        mock_db.__getitem__.return_value = collection
        return collection

    @pytest.fixture
    def sample_document_data(self):
        """Create sample document data."""
        return {
            "_id": ObjectId(),
            "user_id": ObjectId(),
            "property_id": ObjectId(),
            "contract_id": None,
            "filename": "lease_agreement.pdf",
            "file_type": "application/pdf",
            "storage_path": "/storage/documents/lease_agreement.pdf",
            "document_type": "lease",
            "uploaded_at": datetime.utcnow()
        }

    def test_create_document(self, mock_document_collection, sample_document_data):
        """Test creating a new document."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        document_data = {
            "user_id": str(sample_document_data["user_id"]),
            "property_id": str(sample_document_data["property_id"]),
            "filename": sample_document_data["filename"],
            "file_type": sample_document_data["file_type"],
            "storage_path": sample_document_data["storage_path"],
            "document_type": sample_document_data["document_type"]
        }
        mock_document_collection.insert_one.return_value.inserted_id = sample_document_data["_id"]

        # Act
        result = service.create_document(document_data)

        # Assert
        assert result["_id"] == sample_document_data["_id"]
        assert result["user_id"] == sample_document_data["user_id"]
        assert result["filename"] == document_data["filename"]
        mock_document_collection.insert_one.assert_called_once()

    def test_get_document_by_id(self, mock_document_collection, sample_document_data):
        """Test retrieving a document by ID."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        mock_document_collection.find_one.return_value = sample_document_data

        # Act
        result = service.get_document_by_id(str(sample_document_data["_id"]))

        # Assert
        assert result == sample_document_data
        mock_document_collection.find_one.assert_called_once_with(
            {"_id": sample_document_data["_id"]}
        )

    def test_get_document_by_id_not_found(self, mock_document_collection):
        """Test retrieving a non-existent document by ID."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        mock_document_collection.find_one.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.get_document_by_id(str(ObjectId()))
        
        assert exc_info.value.status_code == 404
        assert "Document not found" in str(exc_info.value.detail)

    def test_get_documents_by_user(self, mock_document_collection, sample_document_data):
        """Test retrieving documents by user ID."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        mock_document_collection.find.return_value = [sample_document_data]

        # Act
        result = service.get_documents_by_user(str(sample_document_data["user_id"]))

        # Assert
        assert len(result) == 1
        assert result[0] == sample_document_data
        mock_document_collection.find.assert_called_once_with(
            {"user_id": sample_document_data["user_id"]}
        )

    def test_get_documents_by_property(self, mock_document_collection, sample_document_data):
        """Test retrieving documents by property ID."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        mock_document_collection.find.return_value = [sample_document_data]

        # Act
        result = service.get_documents_by_property(str(sample_document_data["property_id"]))

        # Assert
        assert len(result) == 1
        assert result[0] == sample_document_data
        mock_document_collection.find.assert_called_once_with(
            {"property_id": sample_document_data["property_id"]}
        )

    def test_get_documents_by_contract(self, mock_document_collection, sample_document_data):
        """Test retrieving documents by contract ID."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        contract_id = ObjectId()
        sample_document_data["contract_id"] = contract_id
        mock_document_collection.find.return_value = [sample_document_data]

        # Act
        result = service.get_documents_by_contract(str(contract_id))

        # Assert
        assert len(result) == 1
        assert result[0] == sample_document_data
        mock_document_collection.find.assert_called_once_with(
            {"contract_id": contract_id}
        )

    def test_update_document(self, mock_document_collection, sample_document_data):
        """Test updating a document."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        update_data = {
            "filename": "updated_lease.pdf",
            "document_type": "updated_lease"
        }
        mock_document_collection.find_one_and_update.return_value = {
            **sample_document_data,
            **update_data
        }

        # Act
        result = service.update_document(str(sample_document_data["_id"]), update_data)

        # Assert
        assert result["filename"] == update_data["filename"]
        assert result["document_type"] == update_data["document_type"]
        mock_document_collection.find_one_and_update.assert_called_once()

    def test_update_document_not_found(self, mock_document_collection):
        """Test updating a non-existent document."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        mock_document_collection.find_one_and_update.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.update_document(str(ObjectId()), {"filename": "updated.pdf"})
        
        assert exc_info.value.status_code == 404
        assert "Document not found" in str(exc_info.value.detail)

    def test_delete_document(self, mock_document_collection, sample_document_data):
        """Test deleting a document."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        mock_document_collection.delete_one.return_value.deleted_count = 1

        # Act
        service.delete_document(str(sample_document_data["_id"]))

        # Assert
        mock_document_collection.delete_one.assert_called_once_with(
            {"_id": sample_document_data["_id"]}
        )

    def test_delete_document_not_found(self, mock_document_collection):
        """Test deleting a non-existent document."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        mock_document_collection.delete_one.return_value.deleted_count = 0

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.delete_document(str(ObjectId()))
        
        assert exc_info.value.status_code == 404
        assert "Document not found" in str(exc_info.value.detail)

    def test_list_documents(self, mock_document_collection, sample_document_data):
        """Test listing documents with filters."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        mock_document_collection.find.return_value = [sample_document_data]
        filters = {
            "document_type": "lease",
            "user_id": str(sample_document_data["user_id"])
        }

        # Act
        result = service.list_documents(filters)

        # Assert
        assert len(result) == 1
        assert result[0] == sample_document_data
        mock_document_collection.find.assert_called_once()

    def test_list_documents_empty(self, mock_document_collection):
        """Test listing documents when none match the filters."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        mock_document_collection.find.return_value = []

        # Act
        result = service.list_documents({})

        # Assert
        assert len(result) == 0
        mock_document_collection.find.assert_called_once()

    def test_update_document_type(self, mock_document_collection, sample_document_data):
        """Test updating a document's type."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        new_type = "identification"
        mock_document_collection.find_one_and_update.return_value = {
            **sample_document_data,
            "document_type": new_type
        }

        # Act
        result = service.update_document_type(
            str(sample_document_data["_id"]),
            new_type
        )

        # Assert
        assert result["document_type"] == new_type
        mock_document_collection.find_one_and_update.assert_called_once()

    def test_update_document_type_invalid(self, mock_document_collection, sample_document_data):
        """Test updating a document's type with an invalid type."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        invalid_type = "invalid_type"

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.update_document_type(
                str(sample_document_data["_id"]),
                invalid_type
            )
        
        assert exc_info.value.status_code == 400
        assert "Invalid document type" in str(exc_info.value.detail)
        mock_document_collection.find_one_and_update.assert_not_called()

    def test_get_document_statistics(self, mock_document_collection):
        """Test getting document statistics."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        mock_document_collection.count_documents.side_effect = [20, 5, 10, 5]  # total, leases, ids, contracts

        # Act
        result = service.get_document_statistics()

        # Assert
        assert result["total_documents"] == 20
        assert result["lease_documents"] == 5
        assert result["id_documents"] == 10
        assert result["contract_documents"] == 5
        assert mock_document_collection.count_documents.call_count == 4

    def test_search_documents(self, mock_document_collection, sample_document_data):
        """Test searching documents by filename."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        search_text = "lease"
        mock_document_collection.find.return_value = [sample_document_data]

        # Act
        result = service.search_documents(search_text)

        # Assert
        assert len(result) == 1
        assert result[0] == sample_document_data
        mock_document_collection.find.assert_called_once()

    def test_update_storage_path(self, mock_document_collection, sample_document_data):
        """Test updating a document's storage path."""
        # Arrange
        from app.services.document_service import DocumentService
        service = DocumentService(mock_document_collection)
        new_path = "/storage/documents/new_location/lease.pdf"
        mock_document_collection.find_one_and_update.return_value = {
            **sample_document_data,
            "storage_path": new_path
        }

        # Act
        result = service.update_storage_path(
            str(sample_document_data["_id"]),
            new_path
        )

        # Assert
        assert result["storage_path"] == new_path
        mock_document_collection.find_one_and_update.assert_called_once() 