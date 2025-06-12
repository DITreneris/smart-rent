"""
Tests for the TransactionMonitoringService.
"""
import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from app.services.transaction_monitoring import TransactionMonitoringService
from app.providers.web3 import TransactionStatus
from app.services.verification import VerificationResult

# Mock transaction hash
MOCK_TX_HASH = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

@pytest.fixture
def mock_web3_provider():
    """Create a mock Web3Provider."""
    with patch('app.services.transaction_monitoring.Web3Provider') as mock:
        provider_instance = AsyncMock()
        
        # Configure the mock to return a confirmed transaction status
        status = TransactionStatus(
            tx_hash=MOCK_TX_HASH,
            confirmed=True,
            block_number=12345678,
            confirmations=15,
            receipt={"status": 1, "blockNumber": 12345678}
        )
        provider_instance.get_transaction_status.return_value = status
        
        mock.return_value = provider_instance
        yield mock

@pytest.fixture
def mock_hyperledger_client():
    """Create a mock HyperledgerClient."""
    with patch('app.services.transaction_monitoring.HyperledgerClient') as mock:
        client_instance = AsyncMock()
        client_instance.verify_transaction.return_value = True
        mock.return_value = client_instance
        yield mock

@pytest.fixture
def mock_crypto_client():
    """Create a mock CryptoNetworkClient."""
    with patch('app.services.transaction_monitoring.CryptoNetworkClient') as mock:
        client_instance = AsyncMock()
        client_instance.verify_transaction.return_value = True
        client_instance.get_transaction_details.return_value = {
            "hash": MOCK_TX_HASH,
            "network": "ethereum",
            "status": "confirmed",
            "confirmations": 15
        }
        mock.return_value = client_instance
        yield mock

@pytest.mark.asyncio
async def test_transaction_monitoring_success(
    mock_web3_provider, 
    mock_hyperledger_client, 
    mock_crypto_client
):
    """Test successful transaction monitoring."""
    # Create success callback mock
    on_success = AsyncMock()
    
    # Create service
    service = TransactionMonitoringService()
    
    # Monitor transaction
    result = await service.monitor_transaction(
        MOCK_TX_HASH,
        on_success=on_success
    )
    
    # Assertions
    assert result is True
    on_success.assert_called_once()
    
    tx_status = service.get_transaction_status(MOCK_TX_HASH)
    assert tx_status["status"] == "verified"

@pytest.mark.asyncio
async def test_transaction_verification_failure(
    mock_web3_provider, 
    mock_hyperledger_client, 
    mock_crypto_client
):
    """Test failed transaction verification."""
    # Configure hyperledger mock to fail verification
    mock_hyperledger_client.return_value.verify_transaction.return_value = False
    
    # Create callbacks
    on_success = AsyncMock()
    on_failure = AsyncMock()
    
    # Create service
    service = TransactionMonitoringService()
    
    # Monitor transaction
    result = await service.monitor_transaction(
        MOCK_TX_HASH,
        on_success=on_success,
        on_failure=on_failure
    )
    
    # Assertions
    assert result is False
    on_success.assert_not_called()
    on_failure.assert_called_once()
    
    tx_status = service.get_transaction_status(MOCK_TX_HASH)
    assert tx_status["status"] == "verification_failed"

@pytest.mark.asyncio
async def test_transaction_monitoring_timeout(
    mock_web3_provider
):
    """Test transaction monitoring timeout."""
    # Configure web3 provider to return unconfirmed transaction
    mock_web3_provider.return_value.get_transaction_status.return_value = TransactionStatus(
        tx_hash=MOCK_TX_HASH,
        confirmed=False,
        block_number=None,
        confirmations=0
    )
    
    # Configure service with short timeout
    with patch('app.services.transaction_monitoring.settings') as mock_settings:
        mock_settings.TX_POLLING_INTERVAL = 0.1
        mock_settings.TX_MAX_ATTEMPTS = 3
        
        # Create service with mocked settings
        service = TransactionMonitoringService()
        
        # Create callback
        on_failure = AsyncMock()
        
        # Monitor transaction
        result = await service.monitor_transaction(
            MOCK_TX_HASH,
            on_failure=on_failure
        )
        
        # Assertions
        assert result is False
        on_failure.assert_called_once()
        
        tx_status = service.get_transaction_status(MOCK_TX_HASH)
        assert tx_status["status"] == "timeout"

@pytest.mark.asyncio
async def test_get_transaction_status():
    """Test getting transaction status."""
    # Create service
    service = TransactionMonitoringService()
    
    # Add a mock transaction
    service.active_transactions[MOCK_TX_HASH] = {
        "status": "verified",
        "attempts": 5,
        "start_time": "2025-04-01T12:00:00Z",
        "last_checked": "2025-04-01T12:01:00Z",
        "confirmations": 15
    }
    
    # Get status
    status = service.get_transaction_status(MOCK_TX_HASH)
    
    # Assertions
    assert status["status"] == "verified"
    assert status["attempts"] == 5
    assert status["confirmations"] == 15

@pytest.mark.asyncio
async def test_cancel_monitoring():
    """Test cancelling transaction monitoring."""
    # Create service
    service = TransactionMonitoringService()
    
    # Add a mock transaction
    service.active_transactions[MOCK_TX_HASH] = {
        "status": "pending",
        "attempts": 2
    }
    
    # Cancel monitoring
    result = await service.cancel_monitoring(MOCK_TX_HASH)
    
    # Assertions
    assert result is True
    assert service.active_transactions[MOCK_TX_HASH]["status"] == "cancelled"
    
    # Try cancelling non-existent transaction
    result = await service.cancel_monitoring("0xnonexistent")
    assert result is False 