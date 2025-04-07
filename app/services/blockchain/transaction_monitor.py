"""
Transaction monitoring service for SmartRent platform.
Handles cross-chain transaction monitoring and verification.
"""
from typing import Dict, Optional, Callable
import asyncio
import logging
from datetime import datetime
from .solana import SolanaService
from .hyperledger import HyperledgerService

logger = logging.getLogger(__name__)

class TransactionMonitor:
    """Monitors and verifies transactions across multiple chains."""
    
    def __init__(
        self,
        solana_service: SolanaService,
        hyperledger_service: HyperledgerService,
        config: Dict
    ):
        """Initialize transaction monitor with blockchain services."""
        self.solana = solana_service
        self.hyperledger = hyperledger_service
        self.polling_interval = config.get('polling_interval', 5)  # seconds
        self.max_retries = config.get('max_retries', 30)
        self.callbacks = {}
        
    async def monitor_transaction(
        self,
        tx_hash: str,
        callback: Optional[Callable] = None
    ) -> None:
        """Start monitoring a transaction."""
        retry_count = 0
        
        while retry_count < self.max_retries:
            # Check Solana transaction
            solana_status = await self.solana.verify_transaction(tx_hash)
            
            if solana_status['verified']:
                # Record in Hyperledger
                hyperledger_result = await self.hyperledger.record_transaction(
                    {
                        'tx_hash': tx_hash,
                        'timestamp': datetime.utcnow().isoformat(),
                        'status': 'confirmed'
                    },
                    tx_hash
                )
                
                if hyperledger_result['success']:
                    if callback:
                        await callback({
                            'success': True,
                            'solana_status': solana_status,
                            'hyperledger_id': hyperledger_result['fabric_id']
                        })
                    return
                    
            retry_count += 1
            await asyncio.sleep(self.polling_interval)
            
        # If we get here, transaction failed to confirm
        if callback:
            await callback({
                'success': False,
                'error': 'Transaction confirmation timeout'
            })
            
    async def verify_cross_chain(self, tx_hash: str) -> Dict:
        """Verify transaction status across all chains."""
        try:
            # Get Solana status
            solana_status = await self.solana.verify_transaction(tx_hash)
            
            # Get Hyperledger record
            hyperledger_status = await self.hyperledger.query_transaction(tx_hash)
            
            return {
                'success': True,
                'solana': solana_status,
                'hyperledger': hyperledger_status,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Cross-chain verification failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    async def register_callback(
        self,
        tx_hash: str,
        callback: Callable
    ) -> None:
        """Register a callback for transaction updates."""
        self.callbacks[tx_hash] = callback
        
    async def start_monitoring(self, tx_hash: str) -> None:
        """Start monitoring a transaction with registered callback."""
        callback = self.callbacks.get(tx_hash)
        await self.monitor_transaction(tx_hash, callback)
        
    async def process_transaction_batch(
        self,
        transactions: list[Dict]
    ) -> Dict:
        """Process a batch of transactions."""
        results = []
        
        for tx in transactions:
            try:
                # Verify on Solana
                solana_status = await self.solana.verify_transaction(
                    tx['tx_hash']
                )
                
                if solana_status['verified']:
                    # Record in Hyperledger
                    hyperledger_result = await self.hyperledger.record_transaction(
                        tx,
                        tx['tx_hash']
                    )
                    
                    results.append({
                        'tx_hash': tx['tx_hash'],
                        'success': True,
                        'solana_status': solana_status,
                        'hyperledger_id': hyperledger_result.get('fabric_id')
                    })
                else:
                    results.append({
                        'tx_hash': tx['tx_hash'],
                        'success': False,
                        'error': 'Transaction not verified on Solana'
                    })
            except Exception as e:
                results.append({
                    'tx_hash': tx['tx_hash'],
                    'success': False,
                    'error': str(e)
                })
                
        return {
            'success': True,
            'results': results,
            'timestamp': datetime.utcnow().isoformat()
        }
        
    def stop_monitoring(self, tx_hash: str) -> None:
        """Stop monitoring a transaction."""
        if tx_hash in self.callbacks:
            del self.callbacks[tx_hash] 