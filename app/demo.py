"""
Demonstration script for TransactionMonitoringService.
"""
import asyncio
import logging
from app.services.transaction_monitoring import TransactionMonitoringService
from app.services.verification import VerificationResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Mock transaction hash for demonstration
MOCK_TX_HASH = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

# Define callbacks
async def on_success(tx_hash, verification_result):
    """Handle successful transaction verification."""
    logger.info(f"✅ Transaction {tx_hash} successfully verified!")
    logger.info(f"Verification details: {verification_result.to_dict()}")

async def on_failure(tx_hash, message, verification_result):
    """Handle failed transaction verification."""
    logger.error(f"❌ Transaction {tx_hash} verification failed: {message}")
    if verification_result:
        logger.error(f"Verification details: {verification_result.to_dict()}")

async def on_confirmation(tx_hash, status):
    """Handle transaction confirmation."""
    logger.info(f"💫 Transaction {tx_hash} confirmed on blockchain with {status.confirmations} confirmations")

async def main():
    """Run the demonstration."""
    logger.info("🚀 Starting TransactionMonitoringService demonstration")
    
    # Create service
    service = TransactionMonitoringService()
    
    # Start monitoring a mock transaction
    logger.info(f"Monitoring transaction: {MOCK_TX_HASH}")
    await service.monitor_transaction(
        MOCK_TX_HASH,
        on_success=on_success,
        on_failure=on_failure,
        on_confirmation=on_confirmation
    )
    
    # Show active transactions
    active_txs = service.get_active_transactions()
    logger.info(f"Active transactions: {len(active_txs)}")
    for tx_hash, tx_data in active_txs.items():
        logger.info(f"Transaction {tx_hash}: {tx_data['status']}")
    
    logger.info("✨ Demonstration completed")

if __name__ == "__main__":
    asyncio.run(main()) 