"""
Unit tests for the ProposalService.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from bson import ObjectId
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError

class TestProposalService:
    """Test cases for the ProposalService."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database."""
        return Mock()

    @pytest.fixture
    def mock_proposal_collection(self, mock_db):
        """Create a mock proposal collection."""
        collection = Mock()
        mock_db.__getitem__.return_value = collection
        return collection

    @pytest.fixture
    def sample_proposal_data(self):
        """Create sample proposal data."""
        return {
            "_id": ObjectId(),
            "property_id": ObjectId(),
            "tenant_id": ObjectId(),
            "landlord_id": ObjectId(),
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow(),
            "offer_amount": 1500.00,
            "status": "pending",
            "terms": {
                "deposit": 1500.00,
                "payment_schedule": "monthly",
                "special_conditions": "Pets allowed with additional deposit"
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

    def test_create_proposal(self, mock_proposal_collection, sample_proposal_data):
        """Test creating a new proposal."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        proposal_data = {
            "property_id": str(sample_proposal_data["property_id"]),
            "tenant_id": str(sample_proposal_data["tenant_id"]),
            "landlord_id": str(sample_proposal_data["landlord_id"]),
            "start_date": sample_proposal_data["start_date"],
            "end_date": sample_proposal_data["end_date"],
            "offer_amount": sample_proposal_data["offer_amount"],
            "terms": sample_proposal_data["terms"]
        }
        mock_proposal_collection.insert_one.return_value.inserted_id = sample_proposal_data["_id"]

        # Act
        result = service.create_proposal(proposal_data)

        # Assert
        assert result["_id"] == sample_proposal_data["_id"]
        assert result["property_id"] == sample_proposal_data["property_id"]
        assert result["status"] == "pending"
        mock_proposal_collection.insert_one.assert_called_once()

    def test_get_proposal_by_id(self, mock_proposal_collection, sample_proposal_data):
        """Test retrieving a proposal by ID."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        mock_proposal_collection.find_one.return_value = sample_proposal_data

        # Act
        result = service.get_proposal_by_id(str(sample_proposal_data["_id"]))

        # Assert
        assert result == sample_proposal_data
        mock_proposal_collection.find_one.assert_called_once_with(
            {"_id": sample_proposal_data["_id"]}
        )

    def test_get_proposal_by_id_not_found(self, mock_proposal_collection):
        """Test retrieving a non-existent proposal by ID."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        mock_proposal_collection.find_one.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.get_proposal_by_id(str(ObjectId()))
        
        assert exc_info.value.status_code == 404
        assert "Proposal not found" in str(exc_info.value.detail)

    def test_get_proposals_by_property(self, mock_proposal_collection, sample_proposal_data):
        """Test retrieving proposals by property ID."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        mock_proposal_collection.find.return_value = [sample_proposal_data]

        # Act
        result = service.get_proposals_by_property(str(sample_proposal_data["property_id"]))

        # Assert
        assert len(result) == 1
        assert result[0] == sample_proposal_data
        mock_proposal_collection.find.assert_called_once_with(
            {"property_id": sample_proposal_data["property_id"]}
        )

    def test_get_proposals_by_tenant(self, mock_proposal_collection, sample_proposal_data):
        """Test retrieving proposals by tenant ID."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        mock_proposal_collection.find.return_value = [sample_proposal_data]

        # Act
        result = service.get_proposals_by_tenant(str(sample_proposal_data["tenant_id"]))

        # Assert
        assert len(result) == 1
        assert result[0] == sample_proposal_data
        mock_proposal_collection.find.assert_called_once_with(
            {"tenant_id": sample_proposal_data["tenant_id"]}
        )

    def test_get_proposals_by_landlord(self, mock_proposal_collection, sample_proposal_data):
        """Test retrieving proposals by landlord ID."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        mock_proposal_collection.find.return_value = [sample_proposal_data]

        # Act
        result = service.get_proposals_by_landlord(str(sample_proposal_data["landlord_id"]))

        # Assert
        assert len(result) == 1
        assert result[0] == sample_proposal_data
        mock_proposal_collection.find.assert_called_once_with(
            {"landlord_id": sample_proposal_data["landlord_id"]}
        )

    def test_update_proposal(self, mock_proposal_collection, sample_proposal_data):
        """Test updating a proposal."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        update_data = {
            "offer_amount": 1600.00,
            "terms": {
                "deposit": 1600.00,
                "payment_schedule": "monthly",
                "special_conditions": "No pets allowed"
            }
        }
        mock_proposal_collection.find_one_and_update.return_value = {
            **sample_proposal_data,
            **update_data
        }

        # Act
        result = service.update_proposal(str(sample_proposal_data["_id"]), update_data)

        # Assert
        assert result["offer_amount"] == update_data["offer_amount"]
        assert result["terms"]["special_conditions"] == update_data["terms"]["special_conditions"]
        mock_proposal_collection.find_one_and_update.assert_called_once()

    def test_update_proposal_not_found(self, mock_proposal_collection):
        """Test updating a non-existent proposal."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        mock_proposal_collection.find_one_and_update.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.update_proposal(str(ObjectId()), {"offer_amount": 1600.00})
        
        assert exc_info.value.status_code == 404
        assert "Proposal not found" in str(exc_info.value.detail)

    def test_delete_proposal(self, mock_proposal_collection, sample_proposal_data):
        """Test deleting a proposal."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        mock_proposal_collection.delete_one.return_value.deleted_count = 1

        # Act
        service.delete_proposal(str(sample_proposal_data["_id"]))

        # Assert
        mock_proposal_collection.delete_one.assert_called_once_with(
            {"_id": sample_proposal_data["_id"]}
        )

    def test_delete_proposal_not_found(self, mock_proposal_collection):
        """Test deleting a non-existent proposal."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        mock_proposal_collection.delete_one.return_value.deleted_count = 0

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.delete_proposal(str(ObjectId()))
        
        assert exc_info.value.status_code == 404
        assert "Proposal not found" in str(exc_info.value.detail)

    def test_list_proposals(self, mock_proposal_collection, sample_proposal_data):
        """Test listing proposals with filters."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        mock_proposal_collection.find.return_value = [sample_proposal_data]
        filters = {
            "status": "pending",
            "min_amount": 1000,
            "max_amount": 2000
        }

        # Act
        result = service.list_proposals(filters)

        # Assert
        assert len(result) == 1
        assert result[0] == sample_proposal_data
        mock_proposal_collection.find.assert_called_once()

    def test_list_proposals_empty(self, mock_proposal_collection):
        """Test listing proposals when none match the filters."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        mock_proposal_collection.find.return_value = []

        # Act
        result = service.list_proposals({})

        # Assert
        assert len(result) == 0
        mock_proposal_collection.find.assert_called_once()

    def test_update_proposal_status(self, mock_proposal_collection, sample_proposal_data):
        """Test updating a proposal's status."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        new_status = "accepted"
        mock_proposal_collection.find_one_and_update.return_value = {
            **sample_proposal_data,
            "status": new_status
        }

        # Act
        result = service.update_proposal_status(
            str(sample_proposal_data["_id"]),
            new_status
        )

        # Assert
        assert result["status"] == new_status
        mock_proposal_collection.find_one_and_update.assert_called_once()

    def test_update_proposal_status_invalid(self, mock_proposal_collection, sample_proposal_data):
        """Test updating a proposal's status with an invalid status."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        invalid_status = "invalid_status"

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.update_proposal_status(
                str(sample_proposal_data["_id"]),
                invalid_status
            )
        
        assert exc_info.value.status_code == 400
        assert "Invalid status" in str(exc_info.value.detail)
        mock_proposal_collection.find_one_and_update.assert_not_called()

    def test_get_proposal_statistics(self, mock_proposal_collection):
        """Test getting proposal statistics."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        mock_proposal_collection.count_documents.side_effect = [10, 5, 3, 2]  # total, pending, accepted, rejected

        # Act
        result = service.get_proposal_statistics()

        # Assert
        assert result["total_proposals"] == 10
        assert result["pending_proposals"] == 5
        assert result["accepted_proposals"] == 3
        assert result["rejected_proposals"] == 2
        assert mock_proposal_collection.count_documents.call_count == 4

    def test_get_pending_proposals(self, mock_proposal_collection, sample_proposal_data):
        """Test getting pending proposals."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        mock_proposal_collection.find.return_value = [sample_proposal_data]

        # Act
        result = service.get_pending_proposals()

        # Assert
        assert len(result) == 1
        assert result[0] == sample_proposal_data
        mock_proposal_collection.find.assert_called_once_with({"status": "pending"})

    def test_get_accepted_proposals(self, mock_proposal_collection, sample_proposal_data):
        """Test getting accepted proposals."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        accepted_proposal = {**sample_proposal_data, "status": "accepted"}
        mock_proposal_collection.find.return_value = [accepted_proposal]

        # Act
        result = service.get_accepted_proposals()

        # Assert
        assert len(result) == 1
        assert result[0]["status"] == "accepted"
        mock_proposal_collection.find.assert_called_once_with({"status": "accepted"})

    def test_get_rejected_proposals(self, mock_proposal_collection, sample_proposal_data):
        """Test getting rejected proposals."""
        # Arrange
        from app.services.proposal_service import ProposalService
        service = ProposalService(mock_proposal_collection)
        rejected_proposal = {**sample_proposal_data, "status": "rejected"}
        mock_proposal_collection.find.return_value = [rejected_proposal]

        # Act
        result = service.get_rejected_proposals()

        # Assert
        assert len(result) == 1
        assert result[0]["status"] == "rejected"
        mock_proposal_collection.find.assert_called_once_with({"status": "rejected"}) 