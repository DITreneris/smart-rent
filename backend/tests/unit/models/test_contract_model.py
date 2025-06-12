"""
Unit tests for the Contract model.
"""

import pytest
from bson import ObjectId
from datetime import datetime, timedelta
import mongomock
from pymongo.errors import DuplicateKeyError

class TestContractModel:
    """Test cases for the Contract model."""

    def test_create_contract(self, mock_db, sample_property_data, sample_landlord_data, sample_user_data):
        """Test that a contract can be created with valid data."""
        # Arrange
        contracts = mock_db["contracts"]
        start_date = datetime.utcnow() + timedelta(days=7)
        end_date = start_date + timedelta(days=365)
        
        contract_data = {
            "blockchain_id": "contract_456",
            "property_id": sample_property_data["_id"],
            "landlord_id": sample_landlord_data["_id"],
            "tenant_id": sample_user_data["_id"],
            "start_date": start_date,
            "end_date": end_date,
            "amount": 1200,
            "terms": {
                "deposit": 1200,
                "payment_schedule": "monthly",
                "special_conditions": "No pets allowed"
            },
            "status": "active",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Act
        result = contracts.insert_one(contract_data)
        inserted_contract = contracts.find_one({"_id": result.inserted_id})
        
        # Assert
        assert result.acknowledged
        assert inserted_contract["blockchain_id"] == contract_data["blockchain_id"]
        assert inserted_contract["property_id"] == sample_property_data["_id"]
        assert inserted_contract["landlord_id"] == sample_landlord_data["_id"]
        assert inserted_contract["tenant_id"] == sample_user_data["_id"]
        assert inserted_contract["amount"] == 1200
        assert inserted_contract["status"] == "active"

    def test_find_contract_by_id(self, mock_db, populate_mock_db):
        """Test that a contract can be found by ID."""
        # Arrange
        contracts = mock_db["contracts"]
        sample_contract = populate_mock_db["contracts"][0]
        
        # Act
        found_contract = contracts.find_one({"_id": sample_contract["_id"]})
        
        # Assert
        assert found_contract is not None
        assert found_contract["_id"] == sample_contract["_id"]
        assert found_contract["blockchain_id"] == sample_contract["blockchain_id"]
        assert found_contract["property_id"] == sample_contract["property_id"]

    def test_find_contract_by_blockchain_id(self, mock_db, populate_mock_db):
        """Test that a contract can be found by blockchain ID."""
        # Arrange
        contracts = mock_db["contracts"]
        sample_contract = populate_mock_db["contracts"][0]
        blockchain_id = sample_contract["blockchain_id"]
        
        # Act
        found_contract = contracts.find_one({"blockchain_id": blockchain_id})
        
        # Assert
        assert found_contract is not None
        assert found_contract["_id"] == sample_contract["_id"]
        assert found_contract["blockchain_id"] == blockchain_id

    def test_blockchain_id_uniqueness(self, mock_db, populate_mock_db):
        """Test that blockchain_id uniqueness is enforced."""
        # Arrange
        contracts = mock_db["contracts"]
        sample_contract = populate_mock_db["contracts"][0]
        sample_property = populate_mock_db["properties"][0]
        sample_landlord = populate_mock_db["users"][1]  # Landlord
        sample_tenant = populate_mock_db["users"][0]    # Tenant
        
        start_date = datetime.utcnow() + timedelta(days=14)
        end_date = start_date + timedelta(days=365)
        
        duplicate_contract = {
            "blockchain_id": sample_contract["blockchain_id"],  # Same blockchain_id
            "property_id": sample_property["_id"],
            "landlord_id": sample_landlord["_id"],
            "tenant_id": sample_tenant["_id"],
            "start_date": start_date,
            "end_date": end_date,
            "amount": 1100,
            "terms": {
                "deposit": 1100,
                "payment_schedule": "monthly"
            },
            "status": "active",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Act & Assert
        with pytest.raises(DuplicateKeyError):
            contracts.insert_one(duplicate_contract)

    def test_find_contracts_by_property(self, mock_db, populate_mock_db):
        """Test that contracts can be found by property."""
        # Arrange
        contracts = mock_db["contracts"]
        sample_contract = populate_mock_db["contracts"][0]
        property_id = sample_contract["property_id"]
        
        # Act
        property_contracts = list(contracts.find({"property_id": property_id}))
        
        # Assert
        assert len(property_contracts) == 1
        assert property_contracts[0]["_id"] == sample_contract["_id"]
        assert property_contracts[0]["property_id"] == property_id

    def test_find_contracts_by_landlord(self, mock_db, populate_mock_db):
        """Test that contracts can be found by landlord."""
        # Arrange
        contracts = mock_db["contracts"]
        sample_contract = populate_mock_db["contracts"][0]
        landlord_id = sample_contract["landlord_id"]
        
        # Act
        landlord_contracts = list(contracts.find({"landlord_id": landlord_id}))
        
        # Assert
        assert len(landlord_contracts) == 1
        assert landlord_contracts[0]["_id"] == sample_contract["_id"]
        assert landlord_contracts[0]["landlord_id"] == landlord_id

    def test_find_contracts_by_tenant(self, mock_db, populate_mock_db):
        """Test that contracts can be found by tenant."""
        # Arrange
        contracts = mock_db["contracts"]
        sample_contract = populate_mock_db["contracts"][0]
        tenant_id = sample_contract["tenant_id"]
        
        # Act
        tenant_contracts = list(contracts.find({"tenant_id": tenant_id}))
        
        # Assert
        assert len(tenant_contracts) == 1
        assert tenant_contracts[0]["_id"] == sample_contract["_id"]
        assert tenant_contracts[0]["tenant_id"] == tenant_id

    def test_update_contract_status(self, mock_db, populate_mock_db):
        """Test that a contract's status can be updated."""
        # Arrange
        contracts = mock_db["contracts"]
        sample_contract = populate_mock_db["contracts"][0]
        new_status = "completed"
        
        # Act
        result = contracts.update_one(
            {"_id": sample_contract["_id"]},
            {"$set": {
                "status": new_status,
                "updated_at": datetime.utcnow()
            }}
        )
        updated_contract = contracts.find_one({"_id": sample_contract["_id"]})
        
        # Assert
        assert result.modified_count == 1
        assert updated_contract["status"] == new_status
        assert updated_contract["property_id"] == sample_contract["property_id"]  # Other fields remain unchanged

    def test_update_contract_amount(self, mock_db, populate_mock_db):
        """Test that a contract's amount can be updated."""
        # Arrange
        contracts = mock_db["contracts"]
        sample_contract = populate_mock_db["contracts"][0]
        new_amount = 1100
        
        # Act
        result = contracts.update_one(
            {"_id": sample_contract["_id"]},
            {"$set": {
                "amount": new_amount,
                "updated_at": datetime.utcnow()
            }}
        )
        updated_contract = contracts.find_one({"_id": sample_contract["_id"]})
        
        # Assert
        assert result.modified_count == 1
        assert updated_contract["amount"] == new_amount
        assert updated_contract["status"] == sample_contract["status"]  # Other fields remain unchanged

    def test_update_contract_terms(self, mock_db, populate_mock_db):
        """Test that a contract's terms can be updated."""
        # Arrange
        contracts = mock_db["contracts"]
        sample_contract = populate_mock_db["contracts"][0]
        new_terms = {
            "deposit": sample_contract["terms"]["deposit"],
            "payment_schedule": "bi-weekly",  # Changed from monthly
            "special_conditions": "Pets allowed with additional deposit"  # Changed
        }
        
        # Act
        result = contracts.update_one(
            {"_id": sample_contract["_id"]},
            {"$set": {
                "terms": new_terms,
                "updated_at": datetime.utcnow()
            }}
        )
        updated_contract = contracts.find_one({"_id": sample_contract["_id"]})
        
        # Assert
        assert result.modified_count == 1
        assert updated_contract["terms"]["payment_schedule"] == "bi-weekly"
        assert updated_contract["terms"]["special_conditions"] == "Pets allowed with additional deposit"
        assert updated_contract["amount"] == sample_contract["amount"]  # Other fields remain unchanged

    def test_delete_contract(self, mock_db, populate_mock_db):
        """Test that a contract can be deleted."""
        # Arrange
        contracts = mock_db["contracts"]
        sample_contract = populate_mock_db["contracts"][0]
        initial_count = contracts.count_documents({})
        
        # Act
        result = contracts.delete_one({"_id": sample_contract["_id"]})
        
        # Assert
        assert result.deleted_count == 1
        assert contracts.count_documents({}) == initial_count - 1
        assert contracts.find_one({"_id": sample_contract["_id"]}) is None

    def test_find_contracts_by_status(self, mock_db, populate_mock_db):
        """Test that contracts can be filtered by status."""
        # Arrange
        contracts = mock_db["contracts"]
        sample_contract = populate_mock_db["contracts"][0]  # This one is "active"
        
        # Add another contract with a different status
        completed_contract = sample_contract.copy()
        completed_contract.pop("_id")  # Remove the _id to get a new one
        completed_contract["blockchain_id"] = "contract_789"  # Must be unique
        completed_contract["status"] = "completed"
        contracts.insert_one(completed_contract)
        
        # Act
        active_contracts = list(contracts.find({"status": "active"}))
        completed_contracts = list(contracts.find({"status": "completed"}))
        
        # Assert
        assert len(active_contracts) == 1
        assert len(completed_contracts) == 1
        assert active_contracts[0]["status"] == "active"
        assert completed_contracts[0]["status"] == "completed"

    def test_contract_with_minimal_fields(self, mock_db, sample_property_data, sample_landlord_data, sample_user_data):
        """Test that a contract can be created with minimal required fields."""
        # Arrange
        contracts = mock_db["contracts"]
        start_date = datetime.utcnow() + timedelta(days=7)
        end_date = start_date + timedelta(days=365)
        
        minimal_contract = {
            "property_id": sample_property_data["_id"],
            "landlord_id": sample_landlord_data["_id"],
            "tenant_id": sample_user_data["_id"],
            "start_date": start_date,
            "end_date": end_date,
            "amount": 950,
            "status": "active"
        }
        
        # Act
        result = contracts.insert_one(minimal_contract)
        inserted_contract = contracts.find_one({"_id": result.inserted_id})
        
        # Assert
        assert result.acknowledged
        assert inserted_contract["property_id"] == sample_property_data["_id"]
        assert inserted_contract["landlord_id"] == sample_landlord_data["_id"]
        assert inserted_contract["tenant_id"] == sample_user_data["_id"]
        assert inserted_contract["amount"] == 950
        assert inserted_contract["status"] == "active" 