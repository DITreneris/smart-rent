import os
import json
import asyncio
from web3 import Web3
from web3.middleware import geth_poa_middleware
from functools import lru_cache
from typing import Dict, Any, Optional
import time

# Load environment variables
WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI", "http://localhost:8545")
RENTAL_CONTRACT_ADDRESS = os.getenv("RENTAL_CONTRACT_ADDRESS")

# Connection settings
CONNECTION_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Connection pool - maintain connections to avoid repeated init
_web3_instances = {}
_contract_instances = {}

# Cache for repeated contract calls
contract_call_cache = {}
contract_cache_ttl = 60  # Cache time-to-live in seconds

class BlockchainConnectionError(Exception):
    """Exception raised for blockchain connection errors"""
    pass

@lru_cache(maxsize=8)
def get_contract_abi(contract_name: str) -> Dict[str, Any]:
    """
    Load contract ABI from JSON file with caching for better performance
    """
    try:
        # Try loading from contracts directory
        contract_dir = os.path.join(os.path.dirname(__file__), '..', 'contracts')
        contract_file = os.path.join(contract_dir, f'{contract_name}.json')
        
        if not os.path.exists(contract_file):
            # Try alternative location
            contract_file = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ethereum', 'artifacts', 'contracts', f'{contract_name}.sol', f'{contract_name}.json')
        
        with open(contract_file, 'r') as f:
            contract_data = json.load(f)
            
        # Handle different ABI formats (Hardhat vs Truffle)
        if 'abi' in contract_data:
            return contract_data['abi']
        else:
            return contract_data
    except Exception as e:
        raise ValueError(f"Failed to load contract ABI for {contract_name}: {str(e)}")

async def get_web3(provider_uri: Optional[str] = None) -> Web3:
    """
    Get or create a Web3 instance with connection pooling
    """
    # Use the specified provider URI or default
    provider_uri = provider_uri or WEB3_PROVIDER_URI
    
    # Check if we already have a connection for this provider
    if provider_uri in _web3_instances:
        w3 = _web3_instances[provider_uri]
        # Check connection health
        if w3.is_connected():
            return w3
    
    # Create new connection with retries
    for attempt in range(MAX_RETRIES):
        try:
            # Create new Web3 instance
            if provider_uri.startswith(('http://', 'https://')):
                w3 = Web3(Web3.HTTPProvider(provider_uri, request_kwargs={'timeout': CONNECTION_TIMEOUT}))
            elif provider_uri.startswith('ws://'):
                w3 = Web3(Web3.WebsocketProvider(provider_uri))
            else:
                w3 = Web3(Web3.IPCProvider(provider_uri))
            
            # Add middleware for Proof of Authority networks like local Hardhat/Ganache
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            # Check connection
            if w3.is_connected():
                # Store in connection pool
                _web3_instances[provider_uri] = w3
                return w3
            
            # Wait before retrying
            await asyncio.sleep(RETRY_DELAY)
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise BlockchainConnectionError(f"Failed to connect to Ethereum node at {provider_uri}: {str(e)}")
            
            # Wait before retrying
            await asyncio.sleep(RETRY_DELAY)
    
    raise BlockchainConnectionError(f"Could not establish connection to Ethereum node at {provider_uri}")

async def get_contract(contract_name: str, contract_address: Optional[str] = None):
    """
    Get or create a contract instance with connection pooling
    """
    # Use the specified contract address or default
    contract_address = contract_address or RENTAL_CONTRACT_ADDRESS
    
    if not contract_address:
        raise ValueError("Contract address not provided and not set in environment variables")
    
    # Cache key for this contract
    cache_key = f"{contract_name}:{contract_address}"
    
    # Check if we already have this contract instance
    if cache_key in _contract_instances:
        return _contract_instances[cache_key]
    
    # Get Web3 instance
    w3 = await get_web3()
    
    # Load contract ABI
    contract_abi = get_contract_abi(contract_name)
    
    # Create contract instance
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=contract_abi)
    
    # Store in cache
    _contract_instances[cache_key] = contract
    
    return contract

async def cached_contract_call(contract_name: str, method_name: str, *args, **kwargs):
    """
    Call a contract method with caching to reduce blockchain queries
    
    Args:
        contract_name: Name of the contract
        method_name: Name of the contract method to call
        *args, **kwargs: Arguments to pass to the contract method
    
    Returns:
        The result of the contract method call
    """
    # Create cache key from method name and arguments
    cache_key = f"{contract_name}:{method_name}:{str(args)}:{str(kwargs)}"
    
    # Check if we have a cached result
    if cache_key in contract_call_cache:
        result, timestamp = contract_call_cache[cache_key]
        if time.time() - timestamp < contract_cache_ttl:
            return result
    
    # Get contract
    contract = await get_contract(contract_name)
    
    # Call method
    method = getattr(contract.functions, method_name)
    result = await asyncio.to_thread(method(*args, **kwargs).call)
    
    # Cache result
    contract_call_cache[cache_key] = (result, time.time())
    
    return result

async def clean_contract_cache():
    """
    Clean expired entries from the contract call cache
    """
    # Calculate current time
    current_time = time.time()
    
    # Find expired cache keys
    expired_keys = []
    for key, (_, timestamp) in contract_call_cache.items():
        if current_time - timestamp > contract_cache_ttl:
            expired_keys.append(key)
    
    # Remove expired entries
    for key in expired_keys:
        del contract_call_cache[key]

# Periodically clean the cache in the background
async def start_cache_cleaner():
    while True:
        await clean_contract_cache()
        await asyncio.sleep(300)  # Run every 5 minutes

# Start cache cleaner in the background
async def initialize():
    # Start cache cleaner task
    asyncio.create_task(start_cache_cleaner())
    
    # Pre-connect to Ethereum node
    await get_web3()
    
    # Pre-load rental contract
    if RENTAL_CONTRACT_ADDRESS:
        await get_contract("RentalContract") 