"""
Web3 provider for Ethereum blockchain interactions.
"""
from typing import Dict, Any, Optional
from web3 import Web3
from web3.types import TxReceipt
from dataclasses import dataclass
from app.config.settings import settings

@dataclass
class TransactionStatus:
    """Transaction status data class."""
    tx_hash: str
    confirmed: bool
    block_number: Optional[int] = None
    confirmations: int = 0
    receipt: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class Web3Provider:
    """Provider for Web3 interactions."""
    
    def __init__(self):
        """Initialize Web3 provider."""
        self.provider_uri = settings.WEB3_PROVIDER_URI
        self.chain_id = settings.CHAIN_ID
        self.connect()
    
    def connect(self):
        """Connect to Ethereum node."""
        self.w3 = Web3(Web3.HTTPProvider(self.provider_uri))
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to Ethereum node at {self.provider_uri}")
    
    async def get_transaction_status(self, tx_hash: str) -> TransactionStatus:
        """
        Get transaction status.
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            TransactionStatus object with confirmation details
        """
        try:
            # Convert string to bytes if needed
            if isinstance(tx_hash, str) and tx_hash.startswith('0x'):
                tx_hash_hex = tx_hash
            else:
                tx_hash_hex = Web3.to_hex(tx_hash)
            
            # Get transaction
            tx = self.w3.eth.get_transaction(tx_hash_hex)
            if tx is None:
                return TransactionStatus(
                    tx_hash=tx_hash_hex,
                    confirmed=False,
                    error="Transaction not found"
                )
            
            # Check if transaction is mined
            if tx.get('blockNumber') is None:
                return TransactionStatus(
                    tx_hash=tx_hash_hex,
                    confirmed=False
                )
            
            # Get receipt to confirm success
            receipt = self.w3.eth.get_transaction_receipt(tx_hash_hex)
            
            # Get current block for confirmation count
            current_block = self.w3.eth.block_number
            confirmations = 0
            if receipt and receipt.get('blockNumber'):
                confirmations = current_block - receipt.blockNumber
            
            # Consider confirmed after 12 blocks
            is_confirmed = confirmations >= 12
            
            return TransactionStatus(
                tx_hash=tx_hash_hex,
                confirmed=is_confirmed,
                block_number=receipt.blockNumber if receipt else None,
                confirmations=confirmations,
                receipt=dict(receipt) if receipt else None
            )
            
        except Exception as e:
            return TransactionStatus(
                tx_hash=tx_hash,
                confirmed=False,
                error=str(e)
            )
    
    async def send_transaction(self, tx_data: Dict[str, Any]) -> str:
        """
        Send a transaction to the blockchain.
        
        Args:
            tx_data: Transaction data
            
        Returns:
            Transaction hash
        """
        try:
            # Send the transaction
            tx_hash = self.w3.eth.send_transaction(tx_data)
            return Web3.to_hex(tx_hash)
        except Exception as e:
            raise Exception(f"Failed to send transaction: {str(e)}")
    
    async def get_contract(self, address: str, abi: list) -> Any:
        """
        Get contract instance.
        
        Args:
            address: Contract address
            abi: Contract ABI
            
        Returns:
            Contract instance
        """
        return self.w3.eth.contract(address=address, abi=abi) 