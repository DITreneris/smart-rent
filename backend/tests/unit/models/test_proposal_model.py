"""
Unit tests for the Proposal model.
"""

import pytest
from bson import ObjectId
from datetime import datetime, timedelta
import mongomock
from pymongo.errors import DuplicateKeyError

class TestProposalModel:
    """Test cases for the Proposal model."""

    def test_create_proposal(self, mock_db, sample_property_data, sample_user_data):
        """Test that a proposal can be created with valid data."""
        # Arrange
        proposals = mock_db["proposals"]
        start_date = datetime.utcnow() + timedelta(days=7)
        end_date = start_date + timedelta(days=365)
        
        proposal_data = {
            "property_id": sample_property_data["_id"],
            "tenant_id": sample_user_data["_id"],
            "start_date": start_date,
            "end_date": end_date,
            "offer_amount": 1050,
            "status": "pending",
            "terms": {
                "deposit": 1050,
                "payment_schedule": "monthly",
                "special_conditions": "Pets allowed with additional deposit"
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Act
        result = proposals.insert_one(proposal_data)
        inserted_proposal = proposals.find_one({"_id": result.inserted_id})
        
        # Assert
        assert result.acknowledged
        assert inserted_proposal["property_id"] == sample_property_data["_id"]
        assert inserted_proposal["tenant_id"] == sample_user_data["_id"]
        assert inserted_proposal["offer_amount"] == 1050
        assert inserted_proposal["status"] == "pending"
        assert inserted_proposal["terms"]["special_conditions"] == "Pets allowed with additional deposit"

    def test_find_proposal_by_id(self, mock_db, populate_mock_db):
        """Test that a proposal can be found by ID."""
        # Arrange
        proposals = mock_db["proposals"]
        sample_proposal = populate_mock_db["proposals"][0]
        
        # Act
        found_proposal = proposals.find_one({"_id": sample_proposal["_id"]})
        
        # Assert
        assert found_proposal is not None
        assert found_proposal["_id"] == sample_proposal["_id"]
        assert found_proposal["property_id"] == sample_proposal["property_id"]
        assert found_proposal["tenant_id"] == sample_proposal["tenant_id"]

    def test_find_proposals_by_property(self, mock_db, populate_mock_db):
        """Test that proposals can be found by property."""
        # Arrange
        proposals = mock_db["proposals"]
        sample_proposal = populate_mock_db["proposals"][0]
        property_id = sample_proposal["property_id"]
        
        # Act
        property_proposals = list(proposals.find({"property_id": property_id}))
        
        # Assert
        assert len(property_proposals) == 1
        assert property_proposals[0]["_id"] == sample_proposal["_id"]
        assert property_proposals[0]["property_id"] == property_id

    def test_find_proposals_by_tenant(self, mock_db, populate_mock_db):
        """Test that proposals can be found by tenant."""
        # Arrange
        proposals = mock_db["proposals"]
        sample_proposal = populate_mock_db["proposals"][0]
        tenant_id = sample_proposal["tenant_id"]
        
        # Act
        tenant_proposals = list(proposals.find({"tenant_id": tenant_id}))
        
        # Assert
        assert len(tenant_proposals) == 1
        assert tenant_proposals[0]["_id"] == sample_proposal["_id"]
        assert tenant_proposals[0]["tenant_id"] == tenant_id

    def test_update_proposal_status(self, mock_db, populate_mock_db):
        """Test that a proposal's status can be updated."""
        # Arrange
        proposals = mock_db["proposals"]
        sample_proposal = populate_mock_db["proposals"][0]
        new_status = "accepted"
        
        # Act
        result = proposals.update_one(
            {"_id": sample_proposal["_id"]},
            {"$set": {
                "status": new_status,
                "updated_at": datetime.utcnow()
            }}
        )
        updated_proposal = proposals.find_one({"_id": sample_proposal["_id"]})
        
        # Assert
        assert result.modified_count == 1
        assert updated_proposal["status"] == new_status
        assert updated_proposal["property_id"] == sample_proposal["property_id"]  # Other fields remain unchanged

    def test_update_proposal_offer(self, mock_db, populate_mock_db):
        """Test that a proposal's offer amount can be updated."""
        # Arrange
        proposals = mock_db["proposals"]
        sample_proposal = populate_mock_db["proposals"][0]
        new_offer_amount = 1100
        
        # Act
        result = proposals.update_one(
            {"_id": sample_proposal["_id"]},
            {"$set": {
                "offer_amount": new_offer_amount,
                "terms.deposit": new_offer_amount,
                "updated_at": datetime.utcnow()
            }}
        )
        updated_proposal = proposals.find_one({"_id": sample_proposal["_id"]})
        
        # Assert
        assert result.modified_count == 1
        assert updated_proposal["offer_amount"] == new_offer_amount
        assert updated_proposal["terms"]["deposit"] == new_offer_amount
        assert updated_proposal["status"] == sample_proposal["status"]  # Other fields remain unchanged

    def test_delete_proposal(self, mock_db, populate_mock_db):
        """Test that a proposal can be deleted."""
        # Arrange
        proposals = mock_db["proposals"]
        sample_proposal = populate_mock_db["proposals"][0]
        initial_count = proposals.count_documents({})
        
        # Act
        result = proposals.delete_one({"_id": sample_proposal["_id"]})
        
        # Assert
        assert result.deleted_count == 1
        assert proposals.count_documents({}) == initial_count - 1
        assert proposals.find_one({"_id": sample_proposal["_id"]}) is None

    def test_multiple_proposals_per_property(self, mock_db, populate_mock_db, sample_user_data):
        """Test that multiple proposals can be made for the same property."""
        # Arrange
        proposals = mock_db["proposals"]
        sample_proposal = populate_mock_db["proposals"][0]
        sample_property_id = sample_proposal["property_id"]
        
        # Create a new user with a different ID
        new_user_data = sample_user_data.copy()
        new_user_data["_id"] = ObjectId()
        new_user_data["email"] = "another_tenant@example.com"
        new_user_data["wallet_address"] = "0x5432109876abcdef5432109876abcdef54321098"
        
        # Create a new proposal for the same property but from a different tenant
        start_date = datetime.utcnow() + timedelta(days=10)
        end_date = start_date + timedelta(days=365)
        
        second_proposal_data = {
            "property_id": sample_property_id,
            "tenant_id": new_user_data["_id"],
            "start_date": start_date,
            "end_date": end_date,
            "offer_amount": 1100,
            "status": "pending",
            "terms": {
                "deposit": 1100,
                "payment_schedule": "monthly",
                "special_conditions": "None"
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Act
        mock_db["users"].insert_one(new_user_data)  # Add the new user first
        proposals.insert_one(second_proposal_data)
        
        # Act
        property_proposals = list(proposals.find({"property_id": sample_property_id}))
        
        # Assert
        assert len(property_proposals) == 2
        assert any(p["tenant_id"] == sample_proposal["tenant_id"] for p in property_proposals)
        assert any(p["tenant_id"] == new_user_data["_id"] for p in property_proposals)

    def test_find_pending_proposals(self, mock_db, populate_mock_db):
        """Test that pending proposals can be found."""
        # Arrange
        proposals = mock_db["proposals"]
        sample_proposal = populate_mock_db["proposals"][0]  # This one is "pending"
        
        # Add another proposal with a different status
        accepted_proposal = sample_proposal.copy()
        accepted_proposal.pop("_id")  # Remove the _id to get a new one
        accepted_proposal["tenant_id"] = ObjectId()  # Different tenant
        accepted_proposal["status"] = "accepted"
        proposals.insert_one(accepted_proposal)
        
        # Act
        pending_proposals = list(proposals.find({"status": "pending"}))
        accepted_proposals = list(proposals.find({"status": "accepted"}))
        
        # Assert
        assert len(pending_proposals) == 1
        assert len(accepted_proposals) == 1
        assert pending_proposals[0]["status"] == "pending"
        assert accepted_proposals[0]["status"] == "accepted"

    def test_proposal_with_minimal_fields(self, mock_db, sample_property_data, sample_user_data):
        """Test that a proposal can be created with minimal required fields."""
        # Arrange
        proposals = mock_db["proposals"]
        minimal_proposal = {
            "property_id": sample_property_data["_id"],
            "tenant_id": sample_user_data["_id"],
            "offer_amount": 900,
            "status": "pending"
        }
        
        # Act
        result = proposals.insert_one(minimal_proposal)
        inserted_proposal = proposals.find_one({"_id": result.inserted_id})
        
        # Assert
        assert result.acknowledged
        assert inserted_proposal["property_id"] == sample_property_data["_id"]
        assert inserted_proposal["tenant_id"] == sample_user_data["_id"]
        assert inserted_proposal["offer_amount"] == 900
        assert inserted_proposal["status"] == "pending" 