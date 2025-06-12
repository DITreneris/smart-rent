"""
Unit tests for the ContractService.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from bson import ObjectId
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

class TestContractService:
    """Test cases for the ContractService."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database."""
        return Mock()

    @pytest.fixture
    def mock_contract_collection(self, mock_db):
        """Create a mock contract collection."""
        collection = Mock()
        mock_db.__getitem__.return_value = collection
        return collection

    @pytest.fixture
    def sample_contract_data(self):
        """Create sample contract data."""
        return {
            "_id": ObjectId(),
            "property_id": ObjectId(),
            "landlord_id": ObjectId(),
            "tenant_id": ObjectId(),
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow(),
            "monthly_rent": 1500.00,
            "security_deposit": 3000.00,
            "status": "active",
            "blockchain_id": "0x1234567890abcdef",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

    def test_create_contract(self, mock_contract_collection, sample_contract_data):
        """Test creating a new contract."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        contract_data = {
            "property_id": str(sample_contract_data["property_id"]),
            "landlord_id": str(sample_contract_data["landlord_id"]),
            "tenant_id": str(sample_contract_data["tenant_id"]),
            "start_date": sample_contract_data["start_date"],
            "end_date": sample_contract_data["end_date"],
            "monthly_rent": sample_contract_data["monthly_rent"],
            "security_deposit": sample_contract_data["security_deposit"],
            "blockchain_id": sample_contract_data["blockchain_id"]
        }
        mock_contract_collection.insert_one.return_value.inserted_id = sample_contract_data["_id"]

        # Act
        result = service.create_contract(contract_data)

        # Assert
        assert result["_id"] == sample_contract_data["_id"]
        assert result["property_id"] == sample_contract_data["property_id"]
        assert result["status"] == "active"
        mock_contract_collection.insert_one.assert_called_once()

    def test_create_contract_duplicate_blockchain_id(self, mock_contract_collection, sample_contract_data):
        """Test creating a contract with a duplicate blockchain ID."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        contract_data = {
            "property_id": str(ObjectId()),
            "landlord_id": str(ObjectId()),
            "tenant_id": str(ObjectId()),
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow(),
            "monthly_rent": 2000.00,
            "security_deposit": 4000.00,
            "blockchain_id": sample_contract_data["blockchain_id"]
        }
        mock_contract_collection.insert_one.side_effect = DuplicateKeyError("")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.create_contract(contract_data)
        
        assert exc_info.value.status_code == 400
        assert "Blockchain ID already exists" in str(exc_info.value.detail)

    def test_get_contract_by_id(self, mock_contract_collection, sample_contract_data):
        """Test retrieving a contract by ID."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        mock_contract_collection.find_one.return_value = sample_contract_data

        # Act
        result = service.get_contract_by_id(str(sample_contract_data["_id"]))

        # Assert
        assert result == sample_contract_data
        mock_contract_collection.find_one.assert_called_once_with(
            {"_id": sample_contract_data["_id"]}
        )

    def test_get_contract_by_id_not_found(self, mock_contract_collection):
        """Test retrieving a non-existent contract by ID."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        mock_contract_collection.find_one.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.get_contract_by_id(str(ObjectId()))
        
        assert exc_info.value.status_code == 404
        assert "Contract not found" in str(exc_info.value.detail)

    def test_get_contract_by_blockchain_id(self, mock_contract_collection, sample_contract_data):
        """Test retrieving a contract by blockchain ID."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        mock_contract_collection.find_one.return_value = sample_contract_data

        # Act
        result = service.get_contract_by_blockchain_id(sample_contract_data["blockchain_id"])

        # Assert
        assert result == sample_contract_data
        mock_contract_collection.find_one.assert_called_once_with(
            {"blockchain_id": sample_contract_data["blockchain_id"]}
        )

    def test_get_contracts_by_property(self, mock_contract_collection, sample_contract_data):
        """Test retrieving contracts by property ID."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        mock_contract_collection.find.return_value = [sample_contract_data]

        # Act
        result = service.get_contracts_by_property(str(sample_contract_data["property_id"]))

        # Assert
        assert len(result) == 1
        assert result[0] == sample_contract_data
        mock_contract_collection.find.assert_called_once_with(
            {"property_id": sample_contract_data["property_id"]}
        )

    def test_get_contracts_by_landlord(self, mock_contract_collection, sample_contract_data):
        """Test retrieving contracts by landlord ID."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        mock_contract_collection.find.return_value = [sample_contract_data]

        # Act
        result = service.get_contracts_by_landlord(str(sample_contract_data["landlord_id"]))

        # Assert
        assert len(result) == 1
        assert result[0] == sample_contract_data
        mock_contract_collection.find.assert_called_once_with(
            {"landlord_id": sample_contract_data["landlord_id"]}
        )

    def test_get_contracts_by_tenant(self, mock_contract_collection, sample_contract_data):
        """Test retrieving contracts by tenant ID."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        mock_contract_collection.find.return_value = [sample_contract_data]

        # Act
        result = service.get_contracts_by_tenant(str(sample_contract_data["tenant_id"]))

        # Assert
        assert len(result) == 1
        assert result[0] == sample_contract_data
        mock_contract_collection.find.assert_called_once_with(
            {"tenant_id": sample_contract_data["tenant_id"]}
        )

    def test_update_contract(self, mock_contract_collection, sample_contract_data):
        """Test updating a contract."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        update_data = {
            "monthly_rent": 2000.00,
            "security_deposit": 4000.00
        }
        mock_contract_collection.find_one_and_update.return_value = {
            **sample_contract_data,
            **update_data
        }

        # Act
        result = service.update_contract(str(sample_contract_data["_id"]), update_data)

        # Assert
        assert result["monthly_rent"] == update_data["monthly_rent"]
        assert result["security_deposit"] == update_data["security_deposit"]
        mock_contract_collection.find_one_and_update.assert_called_once()

    def test_update_contract_not_found(self, mock_contract_collection):
        """Test updating a non-existent contract."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        mock_contract_collection.find_one_and_update.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.update_contract(str(ObjectId()), {"monthly_rent": 2000.00})
        
        assert exc_info.value.status_code == 404
        assert "Contract not found" in str(exc_info.value.detail)

    def test_delete_contract(self, mock_contract_collection, sample_contract_data):
        """Test deleting a contract."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        mock_contract_collection.delete_one.return_value.deleted_count = 1

        # Act
        service.delete_contract(str(sample_contract_data["_id"]))

        # Assert
        mock_contract_collection.delete_one.assert_called_once_with(
            {"_id": sample_contract_data["_id"]}
        )

    def test_delete_contract_not_found(self, mock_contract_collection):
        """Test deleting a non-existent contract."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        mock_contract_collection.delete_one.return_value.deleted_count = 0

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.delete_contract(str(ObjectId()))
        
        assert exc_info.value.status_code == 404
        assert "Contract not found" in str(exc_info.value.detail)

    def test_list_contracts(self, mock_contract_collection, sample_contract_data):
        """Test listing contracts with filters."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        mock_contract_collection.find.return_value = [sample_contract_data]
        filters = {
            "status": "active",
            "min_rent": 1000,
            "max_rent": 2000
        }

        # Act
        result = service.list_contracts(filters)

        # Assert
        assert len(result) == 1
        assert result[0] == sample_contract_data
        mock_contract_collection.find.assert_called_once()

    def test_list_contracts_empty(self, mock_contract_collection):
        """Test listing contracts when none match the filters."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        mock_contract_collection.find.return_value = []

        # Act
        result = service.list_contracts({})

        # Assert
        assert len(result) == 0
        mock_contract_collection.find.assert_called_once()

    def test_update_contract_status(self, mock_contract_collection, sample_contract_data):
        """Test updating a contract's status."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        new_status = "terminated"
        mock_contract_collection.find_one_and_update.return_value = {
            **sample_contract_data,
            "status": new_status
        }

        # Act
        result = service.update_contract_status(
            str(sample_contract_data["_id"]),
            new_status
        )

        # Assert
        assert result["status"] == new_status
        mock_contract_collection.find_one_and_update.assert_called_once()

    def test_update_contract_status_invalid(self, mock_contract_collection, sample_contract_data):
        """Test updating a contract's status with an invalid status."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        invalid_status = "invalid_status"

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.update_contract_status(
                str(sample_contract_data["_id"]),
                invalid_status
            )
        
        assert exc_info.value.status_code == 400
        assert "Invalid status" in str(exc_info.value.detail)
        mock_contract_collection.find_one_and_update.assert_not_called()

    def test_get_contract_statistics(self, mock_contract_collection):
        """Test getting contract statistics."""
        # Arrange
        from app.services.contract_service import ContractService
        service = ContractService(mock_contract_collection)
        mock_contract_collection.count_documents.side_effect = [10, 5, 3, 2]  # total, active, terminated, pending

        # Act
        result = service.get_contract_statistics()

        # Assert
        assert result["total_contracts"] == 10
        assert result["active_contracts"] == 5
        assert result["terminated_contracts"] == 3
        assert result["pending_contracts"] == 2
        assert mock_contract_collection.count_documents.call_count == 4 