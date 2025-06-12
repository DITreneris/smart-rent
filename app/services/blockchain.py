"""
Service layer for interacting with the blockchain (EVM).
"""

import asyncio
from typing import Dict, Any
import uuid
import json # For parsing ABI if needed
import logging

from web3 import Web3
from web3.middleware import geth_poa_middleware # For PoA chains like Polygon, Rinkeby, Goerli
from eth_account import Account # For loading private key
from app.core.config import settings # Assuming settings are here

logger = logging.getLogger(__name__) # Use logger for better diagnostics

# --- Helper for ABI Loading (Example) ---
# You might load this differently, e.g., directly from settings or a dedicated loader
_contract_abi = None
def get_contract_abi():
    global _contract_abi
    if _contract_abi is None:
        try:
            # Option 1: ABI stored directly in settings (as JSON string or dict)
            if isinstance(settings.CONTRACT_ABI, (dict, list)):
                 _contract_abi = settings.CONTRACT_ABI
            elif isinstance(settings.CONTRACT_ABI, str):
                 _contract_abi = json.loads(settings.CONTRACT_ABI)
            # Option 2: ABI stored in a file specified by settings
            # elif isinstance(settings.CONTRACT_ABI_PATH, str):
            #     with open(settings.CONTRACT_ABI_PATH, 'r') as f:
            #         _contract_abi = json.load(f)
            else:
                 raise ValueError("Contract ABI not configured correctly in settings.")
        except Exception as e:
             logger.error(f"Failed to load contract ABI: {e}")
             raise ValueError(f"Failed to load contract ABI: {e}")
    return _contract_abi
# ----------------------------------------

class BlockchainService:
    def __init__(self):
        logger.info("Initializing BlockchainService...")
        try:
            self.w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL)) # Corrected from RPC_URL
            # self.w3.middleware_onion.inject(geth_poa_middleware, layer=0) # If needed
            if not self.w3.is_connected():
                logger.error(f"Failed to connect to blockchain node at {settings.WEB3_PROVIDER_URL}")
                raise ConnectionError(f"Failed to connect to blockchain node at {settings.WEB3_PROVIDER_URL}")
            logger.info(f"Connected to blockchain node. Chain ID: {self.w3.eth.chain_id}")

            self.account = Account.from_key(settings.PLATFORM_PRIVATE_KEY)
            logger.info(f"Platform wallet loaded: {self.account.address}")

            contract_abi = get_contract_abi()
            contract_address_checksum = Web3.to_checksum_address(settings.CONTRACT_ADDRESS)
            self.contract = self.w3.eth.contract(address=contract_address_checksum, abi=contract_abi)
            logger.info(f"Contract loaded at address: {self.contract.address}")
            logger.info("BlockchainService initialized successfully.")
        except ConnectionError as ce:
            logger.exception("Blockchain connection error during initialization.")
            # Re-raise or handle as appropriate for service instantiation
            raise
        except ValueError as ve: # For issues like invalid private key or ABI config
            logger.exception("Configuration error during BlockchainService initialization.")
            raise
        except Exception as e:
            logger.exception("Unexpected error during BlockchainService initialization.")
            raise

    async def get_platform_address(self) -> str:
        return self.account.address

    async def get_contract(self):
        # Returns the contract instance. Actual type is web3.contract.Contract
        return self.contract

    async def trigger_confirm_rental(self, payload: Dict[str, Any]) -> str:
        """
        Sends a transaction to the SmartRent contract to confirm a rental.
        Actual implementation using web3.py.
        """
        logger.info(f"[BlockchainService] Received confirmation payload: {payload}")

        try:
            # Use instance attributes initialized in __init__
            # No need to re-initialize w3, account, contract here
            
            if not self.w3.is_connected(): # Use self.w3
                logger.error(f"Failed to connect to blockchain node at {settings.WEB3_PROVIDER_URL}") # Use consistent setting name
                raise ConnectionError(f"Failed to connect to blockchain node at {settings.WEB3_PROVIDER_URL}")
            logger.info(f"Connected to blockchain node. Chain ID: {self.w3.eth.chain_id}")

            # Contract is already loaded as self.contract
            logger.info(f"Using contract loaded at address: {self.contract.address}")

            # Account is already loaded as self.account
            sender_address = self.account.address
            logger.info(f"Using platform wallet: {sender_address}")

            # 4. Prepare Function Call Arguments (Type Conversions)
            try:
                 rental_id_bytes = payload['rental_id'] # Assuming already bytes (e.g., uuid.bytes)
                 # Ensure it's exactly 32 bytes if contract requires bytes32
                 if len(rental_id_bytes) != 32:
                      # Pad or hash if necessary - using hashing as safer example
                      import hashlib
                      rental_id_bytes = hashlib.sha256(rental_id_bytes).digest()
                      logger.warning(f"Converted rental_id to bytes32 via SHA256 hash.")
                 
                 property_id_int = int(payload['property_id']) # Assuming conversion done in ProposalService
                 tenant_checksum_addr = Web3.to_checksum_address(payload['tenant_address'])
                 landlord_checksum_addr = Web3.to_checksum_address(payload['landlord_address'])
                 metadata_uri_str = str(payload['metadata_uri'])
            except Exception as e:
                 logger.error(f"Error converting payload arguments for contract call: {e}")
                 raise TypeError(f"Invalid payload data types for contract call: {e}")

            # 5. Build Transaction
            nonce = self.w3.eth.get_transaction_count(sender_address)
            
            # Gas Strategy: Use estimateGas + buffer, or fixed values from settings
            try:
                estimated_gas = self.contract.functions.confirmRental( # Use self.contract
                    rental_id_bytes,
                    property_id_int,
                    tenant_checksum_addr,
                    landlord_checksum_addr,
                    metadata_uri_str
                ).estimate_gas({'from': sender_address})
                gas_limit = int(estimated_gas * 1.2) # Add 20% buffer
            except Exception as e:
                logger.warning(f"Could not estimate gas, using default. Error: {e}")
                gas_limit = settings.DEFAULT_GAS_LIMIT

            gas_price = self.w3.eth.gas_price # Use self.w3
            
            tx_data = {
                'from': sender_address,
                'nonce': nonce,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'chainId': self.w3.eth.chain_id # Use self.w3
            }
            
            logger.info(f"Building transaction with nonce {nonce}, gasLimit {gas_limit}, gasPrice {gas_price}")
            
            transaction = self.contract.functions.confirmRental( # Use self.contract
                 rental_id_bytes,
                 property_id_int,
                 tenant_checksum_addr,
                 landlord_checksum_addr,
                 metadata_uri_str
            ).build_transaction(tx_data)

            # 6. Sign and Send Transaction
            signed_tx = self.w3.eth.account.sign_transaction(transaction, settings.PLATFORM_PRIVATE_KEY) # Use self.w3
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction) # Use self.w3
            logger.info(f"Transaction sent. Hash: {tx_hash.hex()}")

            # 7. (Optional) Wait for Receipt
            # For critical operations, waiting is recommended.
            # Add timeout to prevent indefinite waiting.
            # wait_timeout = settings.TX_WAIT_TIMEOUT # e.g., 120 seconds
            # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=wait_timeout)
            # logger.info(f"Transaction receipt received. Status: {tx_receipt.status}")
            # if tx_receipt.status == 0:
            #     logger.error(f"Transaction {tx_hash.hex()} failed on-chain.")
            #     raise Exception("Transaction failed on-chain (Status 0)")
                
            return tx_hash.hex()

        except ConnectionError as ce:
             logger.exception("Blockchain connection error.")
             raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Blockchain node connection error: {ce}")
        except ValueError as ve:
             logger.exception("Configuration or value error.")
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Blockchain configuration error: {ve}")
        except TypeError as te:
            logger.exception("Payload type error.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid data for blockchain call: {te}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred during blockchain interaction: {e}")
            # Check for specific web3 exceptions if needed
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Blockchain transaction failed: {e}")

    # Add other blockchain interaction methods as needed (e.g., read contract state)