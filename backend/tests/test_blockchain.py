import pytest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import os

from ..app.services.blockchain import (
    load_contract_data,
    deploy_rental_agreement,
    get_agreement_details,
    terminate_agreement,
    complete_agreement
)


@pytest.fixture
def mock_web3():
    """Create a mock Web3 instance for testing."""
    with patch('web3.Web3') as mock_web3:
        # Setup mock for HTTPProvider
        mock_provider = MagicMock()
        mock_web3.HTTPProvider.return_value = mock_provider
        
        # Setup mock for the Web3 instance
        mock_w3 = MagicMock()
        mock_web3.return_value = mock_w3
        
        # Setup mock for eth.account
        mock_account = MagicMock()
        mock_account.address = "0x1234567890123456789012345678901234567890"
        mock_w3.eth.account.from_key.return_value = mock_account
        
        # Setup mock for eth.default_account
        mock_w3.eth.default_account = mock_account.address
        
        # Setup mock for eth.get_transaction_count
        mock_w3.eth.get_transaction_count.return_value = 1
        
        # Setup mock for eth.gas_price
        mock_w3.eth.gas_price = 20000000000
        
        # Setup mock for eth.send_raw_transaction
        mock_tx_hash = MagicMock()
        mock_tx_hash.hex.return_value = "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
        mock_w3.eth.send_raw_transaction.return_value = mock_tx_hash
        
        # Setup mock for eth.wait_for_transaction_receipt
        mock_receipt = MagicMock()
        mock_receipt.contractAddress = "0x0987654321098765432109876543210987654321"
        mock_receipt.blockNumber = 123456
        mock_receipt.status = 1
        mock_w3.eth.wait_for_transaction_receipt.return_value = mock_receipt
        
        yield mock_web3


@pytest.fixture
def mock_contract_files(tmp_path):
    """Create temporary contract files for testing."""
    contracts_dir = tmp_path / "contracts"
    contracts_dir.mkdir()
    
    # Create ABI file
    abi_file = contracts_dir / "RentalAgreement.abi"
    abi_data = [
        {
            "constant": False,
            "inputs": [],
            "name": "getAgreementDetails",
            "outputs": [
                {"name": "landlord", "type": "address"},
                {"name": "tenant", "type": "address"},
                {"name": "propertyId", "type": "uint256"},
                {"name": "startDate", "type": "uint256"},
                {"name": "endDate", "type": "uint256"},
                {"name": "monthlyRent", "type": "uint256"},
                {"name": "securityDeposit", "type": "uint256"},
                {"name": "status", "type": "uint8"},
                {"name": "securityDepositReturned", "type": "bool"}
            ],
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [],
            "name": "terminateAgreement",
            "outputs": [],
            "type": "function"
        },
        {
            "constant": False,
            "inputs": [],
            "name": "completeAgreement",
            "outputs": [],
            "type": "function"
        }
    ]
    abi_file.write_text(json.dumps(abi_data))
    
    # Create bytecode file
    bin_file = contracts_dir / "RentalAgreement.bin"
    bin_file.write_text("0x6080604052...")
    
    # Patch the CONTRACT_DIR to point to our temp directory
    with patch('backend.app.services.blockchain.CONTRACT_DIR', str(contracts_dir)):
        yield str(contracts_dir)


def test_load_contract_data(mock_contract_files):
    """Test loading contract ABI and bytecode."""
    # Test with existing contract
    abi, bytecode = load_contract_data("RentalAgreement")
    assert isinstance(abi, list)
    assert len(abi) == 3
    assert isinstance(bytecode, str)
    assert bytecode.startswith("0x")
    
    # Test with non-existent contract
    with patch('builtins.print') as mock_print:
        abi, bytecode = load_contract_data("NonExistentContract")
        mock_print.assert_called_once()
        assert len(abi) == 0
        assert bytecode == "0x"


@patch('web3.Web3')
def test_deploy_rental_agreement(mock_web3_class, mock_contract_files, mock_web3):
    """Test deploying a rental agreement contract."""
    # Setup the chain of mocks
    mock_web3_instance = mock_web3_class.return_value
    mock_contract = MagicMock()
    mock_web3_instance.eth.contract.return_value = mock_contract
    
    # Setup constructor mock
    mock_constructor = MagicMock()
    mock_contract.constructor.return_value = mock_constructor
    
    # Setup transaction mock
    mock_tx = {'from': '0x1234', 'nonce': 1, 'gas': 2000000, 'gasPrice': 20000000000}
    mock_constructor.build_transaction.return_value = mock_tx
    
    # Setup account mock
    mock_account = MagicMock()
    mock_web3_instance.eth.account.from_key.return_value = mock_account
    
    # Setup signing mock
    mock_signed = MagicMock()
    mock_account.sign_transaction.return_value = mock_signed
    
    # Setup tx receipt mock
    mock_receipt = MagicMock()
    mock_receipt.contractAddress = "0x5678"
    mock_receipt.blockNumber = 12345
    mock_web3_instance.eth.wait_for_transaction_receipt.return_value = mock_receipt
    
    # Call the function
    tenant_address = "0x2345678901234567890123456789012345678901"
    property_id = 1
    start_date = int((datetime.now() + timedelta(days=1)).timestamp())
    end_date = int((datetime.now() + timedelta(days=366)).timestamp())
    monthly_rent = 200000
    
    result = deploy_rental_agreement(tenant_address, property_id, start_date, end_date, monthly_rent)
    
    # Assertions
    assert "contract_address" in result
    assert "tx_hash" in result
    assert "block_number" in result
    assert result["contract_address"] == "0x5678"
    assert isinstance(result["tx_hash"], str)
    assert result["block_number"] == 12345


@patch('web3.Web3')
def test_get_agreement_details(mock_web3_class, mock_contract_files):
    """Test getting agreement details from a contract."""
    # Setup the chain of mocks
    mock_web3_instance = mock_web3_class.return_value
    mock_contract = MagicMock()
    mock_web3_instance.eth.contract.return_value = mock_contract
    
    # Setup functions mock
    mock_functions = MagicMock()
    mock_contract.functions = mock_functions
    
    # Setup getAgreementDetails mock
    mock_get_details = MagicMock()
    mock_functions.getAgreementDetails.return_value = mock_get_details
    
    # Setup call mock with return values
    landlord = "0x1111111111111111111111111111111111111111"
    tenant = "0x2222222222222222222222222222222222222222"
    property_id = 1
    start_date = int(datetime.now().timestamp())
    end_date = int((datetime.now() + timedelta(days=365)).timestamp())
    monthly_rent = 200000
    security_deposit = 400000
    status = 0  # Active
    security_deposit_returned = False
    
    mock_get_details.call.return_value = [
        landlord, tenant, property_id, start_date, end_date,
        monthly_rent, security_deposit, status, security_deposit_returned
    ]
    
    # Call the function
    contract_address = "0xabcdef1234567890abcdef1234567890abcdef12"
    result = get_agreement_details(contract_address)
    
    # Assertions
    assert result["landlord"] == landlord
    assert result["tenant"] == tenant
    assert result["property_id"] == property_id
    assert result["start_date"] == start_date
    assert result["end_date"] == end_date
    assert result["monthly_rent"] == monthly_rent
    assert result["security_deposit"] == security_deposit
    assert result["status"] == status
    assert result["security_deposit_returned"] == security_deposit_returned


@patch('web3.Web3')
def test_terminate_agreement(mock_web3_class, mock_contract_files):
    """Test terminating a rental agreement contract."""
    # Setup the chain of mocks
    mock_web3_instance = mock_web3_class.return_value
    mock_contract = MagicMock()
    mock_web3_instance.eth.contract.return_value = mock_contract
    
    # Setup functions mock
    mock_functions = MagicMock()
    mock_contract.functions = mock_functions
    
    # Setup terminateAgreement mock
    mock_terminate = MagicMock()
    mock_functions.terminateAgreement.return_value = mock_terminate
    
    # Setup transaction mock
    mock_tx = {'from': '0x1234', 'nonce': 1, 'gas': 200000, 'gasPrice': 20000000000}
    mock_terminate.build_transaction.return_value = mock_tx
    
    # Setup account mock
    mock_account = MagicMock()
    mock_web3_instance.eth.account.from_key.return_value = mock_account
    
    # Setup signing mock
    mock_signed = MagicMock()
    mock_account.sign_transaction.return_value = mock_signed
    
    # Setup tx receipt mock
    mock_tx_hash = MagicMock()
    mock_tx_hash.hex.return_value = "0xabcdef1234567890"
    mock_web3_instance.eth.send_raw_transaction.return_value = mock_tx_hash
    
    mock_receipt = MagicMock()
    mock_receipt.blockNumber = 12345
    mock_receipt.status = 1
    mock_web3_instance.eth.wait_for_transaction_receipt.return_value = mock_receipt
    
    # Call the function
    contract_address = "0xabcdef1234567890abcdef1234567890abcdef12"
    result = terminate_agreement(contract_address)
    
    # Assertions
    assert "tx_hash" in result
    assert "block_number" in result
    assert "status" in result
    assert result["tx_hash"] == "0xabcdef1234567890"
    assert result["block_number"] == 12345
    assert result["status"] == 1


@patch('web3.Web3')
def test_complete_agreement(mock_web3_class, mock_contract_files):
    """Test completing a rental agreement contract."""
    # Setup the chain of mocks
    mock_web3_instance = mock_web3_class.return_value
    mock_contract = MagicMock()
    mock_web3_instance.eth.contract.return_value = mock_contract
    
    # Setup functions mock
    mock_functions = MagicMock()
    mock_contract.functions = mock_functions
    
    # Setup completeAgreement mock
    mock_complete = MagicMock()
    mock_functions.completeAgreement.return_value = mock_complete
    
    # Setup transaction mock
    mock_tx = {'from': '0x1234', 'nonce': 1, 'gas': 200000, 'gasPrice': 20000000000}
    mock_complete.build_transaction.return_value = mock_tx
    
    # Setup account mock
    mock_account = MagicMock()
    mock_web3_instance.eth.account.from_key.return_value = mock_account
    
    # Setup signing mock
    mock_signed = MagicMock()
    mock_account.sign_transaction.return_value = mock_signed
    
    # Setup tx receipt mock
    mock_tx_hash = MagicMock()
    mock_tx_hash.hex.return_value = "0xabcdef1234567890"
    mock_web3_instance.eth.send_raw_transaction.return_value = mock_tx_hash
    
    mock_receipt = MagicMock()
    mock_receipt.blockNumber = 12345
    mock_receipt.status = 1
    mock_web3_instance.eth.wait_for_transaction_receipt.return_value = mock_receipt
    
    # Call the function
    contract_address = "0xabcdef1234567890abcdef1234567890abcdef12"
    result = complete_agreement(contract_address)
    
    # Assertions
    assert "tx_hash" in result
    assert "block_number" in result
    assert "status" in result
    assert result["tx_hash"] == "0xabcdef1234567890"
    assert result["block_number"] == 12345
    assert result["status"] == 1 