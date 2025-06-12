"""
Unit tests for the BlockchainService.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from bson import ObjectId
from fastapi import HTTPException
from web3.exceptions import ContractLogicError, TimeoutError

class TestBlockchainService:
    """Test cases for the BlockchainService."""

    @pytest.fixture
    def mock_web3(self):
        """Create a mock Web3 instance."""
        return Mock()

    @pytest.fixture
    def mock_contract(self):
        """Create a mock contract instance."""
        return Mock()

    @pytest.fixture
    def mock_account(self):
        """Create a mock account."""
        return Mock()

    @pytest.fixture
    def sample_contract_data(self):
        """Create sample contract data."""
        return {
            "property_id": str(ObjectId()),
            "landlord_id": str(ObjectId()),
            "tenant_id": str(ObjectId()),
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow(),
            "monthly_rent": 1500.00,
            "security_deposit": 3000.00
        }

    def test_deploy_contract(self, mock_web3, mock_contract, mock_account, sample_contract_data):
        """Test deploying a smart contract."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        mock_contract.constructor.return_value.transact.return_value = "0x1234567890abcdef"
        mock_web3.eth.wait_for_transaction_receipt.return_value = {
            "contractAddress": "0xcontractaddress",
            "status": 1
        }

        # Act
        result = service.deploy_contract(sample_contract_data)

        # Assert
        assert result["contract_address"] == "0xcontractaddress"
        assert result["status"] == "success"
        mock_contract.constructor.assert_called_once()
        mock_web3.eth.wait_for_transaction_receipt.assert_called_once()

    def test_deploy_contract_failure(self, mock_web3, mock_contract, mock_account, sample_contract_data):
        """Test deploying a smart contract with failure."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        mock_contract.constructor.return_value.transact.side_effect = ContractLogicError("Deployment failed")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.deploy_contract(sample_contract_data)
        
        assert exc_info.value.status_code == 500
        assert "Failed to deploy contract" in str(exc_info.value.detail)

    def test_get_contract_details(self, mock_web3, mock_contract, mock_account):
        """Test getting contract details."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xcontractaddress"
        mock_contract.functions.getDetails.return_value.call.return_value = (
            "0xlandlord",
            "0xtenant",
            1500,
            3000,
            1234567890,
            1234567890
        )

        # Act
        result = service.get_contract_details(contract_address)

        # Assert
        assert result["landlord_address"] == "0xlandlord"
        assert result["tenant_address"] == "0xtenant"
        assert result["monthly_rent"] == 1500
        assert result["security_deposit"] == 3000
        mock_contract.functions.getDetails.assert_called_once()

    def test_get_contract_details_not_found(self, mock_web3, mock_contract, mock_account):
        """Test getting details of a non-existent contract."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xinvalidaddress"
        mock_contract.functions.getDetails.return_value.call.side_effect = ContractLogicError("Contract not found")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.get_contract_details(contract_address)
        
        assert exc_info.value.status_code == 404
        assert "Contract not found" in str(exc_info.value.detail)

    def test_update_contract_status(self, mock_web3, mock_contract, mock_account):
        """Test updating contract status."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xcontractaddress"
        new_status = "active"
        mock_contract.functions.updateStatus.return_value.transact.return_value = "0x1234567890abcdef"
        mock_web3.eth.wait_for_transaction_receipt.return_value = {"status": 1}

        # Act
        result = service.update_contract_status(contract_address, new_status)

        # Assert
        assert result["status"] == "success"
        mock_contract.functions.updateStatus.assert_called_once()
        mock_web3.eth.wait_for_transaction_receipt.assert_called_once()

    def test_update_contract_status_failure(self, mock_web3, mock_contract, mock_account):
        """Test updating contract status with failure."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xcontractaddress"
        new_status = "invalid_status"
        mock_contract.functions.updateStatus.return_value.transact.side_effect = ContractLogicError("Invalid status")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.update_contract_status(contract_address, new_status)
        
        assert exc_info.value.status_code == 400
        assert "Invalid status" in str(exc_info.value.detail)

    def test_process_rent_payment(self, mock_web3, mock_contract, mock_account):
        """Test processing a rent payment."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xcontractaddress"
        amount = 1500
        mock_contract.functions.processPayment.return_value.transact.return_value = "0x1234567890abcdef"
        mock_web3.eth.wait_for_transaction_receipt.return_value = {"status": 1}

        # Act
        result = service.process_rent_payment(contract_address, amount)

        # Assert
        assert result["status"] == "success"
        mock_contract.functions.processPayment.assert_called_once()
        mock_web3.eth.wait_for_transaction_receipt.assert_called_once()

    def test_process_rent_payment_failure(self, mock_web3, mock_contract, mock_account):
        """Test processing a rent payment with failure."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xcontractaddress"
        amount = 1000  # Less than monthly rent
        mock_contract.functions.processPayment.return_value.transact.side_effect = ContractLogicError("Insufficient payment")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.process_rent_payment(contract_address, amount)
        
        assert exc_info.value.status_code == 400
        assert "Insufficient payment" in str(exc_info.value.detail)

    def test_get_payment_history(self, mock_web3, mock_contract, mock_account):
        """Test getting payment history."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xcontractaddress"
        mock_contract.functions.getPaymentHistory.return_value.call.return_value = [
            (1234567890, 1500, "0xpaymenthash"),
            (1234567891, 1500, "0xpaymenthash2")
        ]

        # Act
        result = service.get_payment_history(contract_address)

        # Assert
        assert len(result) == 2
        assert result[0]["amount"] == 1500
        mock_contract.functions.getPaymentHistory.assert_called_once()

    def test_get_contract_balance(self, mock_web3, mock_contract, mock_account):
        """Test getting contract balance."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xcontractaddress"
        mock_web3.eth.get_balance.return_value = 3000

        # Act
        result = service.get_contract_balance(contract_address)

        # Assert
        assert result == 3000
        mock_web3.eth.get_balance.assert_called_once_with(contract_address)

    def test_terminate_contract(self, mock_web3, mock_contract, mock_account):
        """Test terminating a contract."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xcontractaddress"
        mock_contract.functions.terminate.return_value.transact.return_value = "0x1234567890abcdef"
        mock_web3.eth.wait_for_transaction_receipt.return_value = {"status": 1}

        # Act
        result = service.terminate_contract(contract_address)

        # Assert
        assert result["status"] == "success"
        mock_contract.functions.terminate.assert_called_once()
        mock_web3.eth.wait_for_transaction_receipt.assert_called_once()

    def test_terminate_contract_failure(self, mock_web3, mock_contract, mock_account):
        """Test terminating a contract with failure."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xcontractaddress"
        mock_contract.functions.terminate.return_value.transact.side_effect = ContractLogicError("Cannot terminate active contract")

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.terminate_contract(contract_address)
        
        assert exc_info.value.status_code == 400
        assert "Cannot terminate contract" in str(exc_info.value.detail)

    def test_get_contract_events(self, mock_web3, mock_contract, mock_account):
        """Test getting contract events."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xcontractaddress"
        event_name = "PaymentProcessed"
        mock_contract.events.PaymentProcessed.createFilter.return_value.get_all_entries.return_value = [
            {"args": {"amount": 1500, "timestamp": 1234567890}}
        ]

        # Act
        result = service.get_contract_events(contract_address, event_name)

        # Assert
        assert len(result) == 1
        assert result[0]["amount"] == 1500
        mock_contract.events.PaymentProcessed.createFilter.assert_called_once()

    def test_validate_contract_address(self, mock_web3, mock_contract, mock_account):
        """Test validating a contract address."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xcontractaddress"
        mock_web3.eth.get_code.return_value = b"contract_code"

        # Act
        result = service.validate_contract_address(contract_address)

        # Assert
        assert result is True
        mock_web3.eth.get_code.assert_called_once_with(contract_address)

    def test_validate_contract_address_invalid(self, mock_web3, mock_contract, mock_account):
        """Test validating an invalid contract address."""
        # Arrange
        from app.services.blockchain_service import BlockchainService
        service = BlockchainService(mock_web3, mock_contract, mock_account)
        contract_address = "0xinvalidaddress"
        mock_web3.eth.get_code.return_value = b""

        # Act
        result = service.validate_contract_address(contract_address)

        # Assert
        assert result is False
        mock_web3.eth.get_code.assert_called_once_with(contract_address) 