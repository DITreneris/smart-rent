"""
Transaction monitoring service for cross-network verification.
"""
import asyncio
import logging
from typing import Dict, Any, Callable, Optional, List
from datetime import datetime
from app.providers.web3 import Web3Provider, TransactionStatus
from app.providers.hyperledger import HyperledgerClient
from app.providers.crypto import CryptoNetworkClient
from app.services.verification import VerificationResult
from app.config.settings import settings

# Set up logging
logger = logging.getLogger(__name__)

class TransactionMonitoringService:
    """Service for monitoring transactions across networks."""
    
    def __init__(self):
        """Initialize transaction monitoring service."""
        self.web3 = Web3Provider()
        self.fabric_client = HyperledgerClient()
        self.crypto_client = CryptoNetworkClient()
        self.polling_interval = settings.TX_POLLING_INTERVAL
        self.max_attempts = settings.TX_MAX_ATTEMPTS
        self.active_transactions = {}
        logger.info("TransactionMonitoringService initialized")
    
    async def monitor_transaction(
        self, 
        tx_hash: str, 
        on_success: Optional[Callable] = None, 
        on_failure: Optional[Callable] = None,
        on_confirmation: Optional[Callable] = None
    ) -> bool:
        """
        Monitor transaction status across networks.
        
        Args:
            tx_hash: Transaction hash
            on_success: Callback for successful verification
            on_failure: Callback for failed verification
            on_confirmation: Callback for blockchain confirmation (before verification)
            
        Returns:
            True if transaction was successfully verified, False otherwise
        """
        logger.info(f"Starting monitoring for transaction {tx_hash}")
        
        # Register transaction as active
        self.active_transactions[tx_hash] = {
            "status": "pending",
            "attempts": 0,
            "start_time": datetime.utcnow(),
            "last_checked": None,
            "confirmations": 0
        }
        
        # Start monitoring loop
        attempts = 0
        while attempts < self.max_attempts:
            try:
                # Update transaction record
                attempts += 1
                self.active_transactions[tx_hash]["attempts"] = attempts
                self.active_transactions[tx_hash]["last_checked"] = datetime.utcnow()
                
                # Log progress periodically
                if attempts % 5 == 0:
                    logger.info(f"Still monitoring transaction {tx_hash}, attempt {attempts}")
                
                # Check status
                status = await self.web3.get_transaction_status(tx_hash)
                self.active_transactions[tx_hash]["confirmations"] = status.confirmations
                
                # Handle confirmation
                if status.confirmed:
                    logger.info(f"Transaction {tx_hash} confirmed on blockchain")
                    self.active_transactions[tx_hash]["status"] = "confirmed"
                    
                    # Call confirmation callback if provided
                    if on_confirmation:
                        await on_confirmation(tx_hash, status)
                    
                    # Proceed with cross-network verification
                    verification_result = await self._verify_across_networks(tx_hash)
                    
                    # Handle verification result
                    if verification_result.success:
                        logger.info(f"Transaction {tx_hash} verified across networks")
                        await self._handle_successful_verification(tx_hash, verification_result)
                        if on_success:
                            await on_success(tx_hash, verification_result)
                        return True
                    else:
                        logger.warning(f"Cross-network verification failed for {tx_hash}")
                        self.active_transactions[tx_hash]["status"] = "verification_failed"
                        self.active_transactions[tx_hash]["verification_result"] = verification_result.to_dict()
                        
                        if on_failure:
                            await on_failure(tx_hash, "Cross-network verification failed", verification_result)
                        return False
                
                # Sleep before next check
                await asyncio.sleep(self.polling_interval)
                
            except Exception as e:
                logger.error(f"Error monitoring transaction {tx_hash}: {str(e)}")
                self.active_transactions[tx_hash]["status"] = "error"
                self.active_transactions[tx_hash]["error"] = str(e)
                
                if on_failure:
                    await on_failure(tx_hash, str(e), None)
                return False
        
        # Handle timeout
        logger.warning(f"Transaction monitoring timed out for {tx_hash}")
        self.active_transactions[tx_hash]["status"] = "timeout"
        if on_failure:
            await on_failure(tx_hash, "Transaction monitoring timed out", None)
        return False
    
    async def _verify_across_networks(self, tx_hash: str) -> VerificationResult:
        """
        Verify transaction across different networks.
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            VerificationResult with details
        """
        logger.info(f"Performing cross-network verification for {tx_hash}")
        
        try:
            # Verify on cryptocurrency network
            crypto_verified = await self.crypto_client.verify_transaction(tx_hash)
            
            # Verify on Hyperledger
            fabric_verified = await self.fabric_client.verify_transaction(tx_hash)
            
            # Get additional details if available
            crypto_details = await self.crypto_client.get_transaction_details(tx_hash)
            
            # Calculate network confirmations
            network_confirmations = crypto_details.get("confirmations", 0)
            
            # Create verification result
            return VerificationResult(
                success=(crypto_verified and fabric_verified),
                network_confirmations=network_confirmations,
                details={
                    "crypto_network": crypto_verified,
                    "hyperledger": fabric_verified,
                    "crypto_details": crypto_details
                }
            )
        
        except Exception as e:
            logger.error(f"Error during cross-network verification: {str(e)}")
            return VerificationResult(
                success=False,
                details={
                    "error": str(e)
                }
            )
    
    async def _handle_successful_verification(self, tx_hash: str, verification_result: VerificationResult):
        """
        Handle successful verification by updating contract state.
        
        Args:
            tx_hash: Transaction hash
            verification_result: Verification result
        """
        logger.info(f"Handling successful verification for {tx_hash}")
        
        # Update transaction record
        self.active_transactions[tx_hash]["status"] = "verified"
        self.active_transactions[tx_hash]["verification_result"] = verification_result.to_dict()
        self.active_transactions[tx_hash]["verified_at"] = datetime.utcnow()
        
        # In a real implementation, this would:
        # 1. Update state in smart contracts
        # 2. Update MongoDB state
        # 3. Emit events for frontend
        
        # For now, just log the success
        logger.info(f"Transaction {tx_hash} successfully verified and processed")
    
    def get_transaction_status(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """
        Get current status of a transaction.
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Transaction status record or None if not found
        """
        return self.active_transactions.get(tx_hash)
    
    def get_active_transactions(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all active transactions.
        
        Returns:
            Dictionary of transaction records
        """
        return self.active_transactions
    
    async def cancel_monitoring(self, tx_hash: str) -> bool:
        """
        Cancel monitoring for a transaction.
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            True if cancelled, False if not found
        """
        if tx_hash in self.active_transactions:
            self.active_transactions[tx_hash]["status"] = "cancelled"
            logger.info(f"Monitoring cancelled for transaction {tx_hash}")
            return True
        return False 