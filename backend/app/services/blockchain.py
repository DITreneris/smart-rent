import json
import os
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
ETHEREUM_NODE_URL = os.getenv("ETHEREUM_NODE_URL")
ETHEREUM_PRIVATE_KEY = os.getenv("ETHEREUM_PRIVATE_KEY")

# Load contract ABI and bytecode
CONTRACT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "contracts")

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider(ETHEREUM_NODE_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # Required for some testnets like Rinkeby

# Account setup
account = w3.eth.account.from_key(ETHEREUM_PRIVATE_KEY)
w3.eth.default_account = account.address


def load_contract_data(contract_name):
    """Load contract ABI and bytecode from JSON files"""
    try:
        # In a real deployment, the ABI and bytecode would be generated from compilation
        # Here we're just simulating this by loading from files
        with open(os.path.join(CONTRACT_DIR, f"{contract_name}.abi"), "r") as f:
            abi = json.load(f)
        
        with open(os.path.join(CONTRACT_DIR, f"{contract_name}.bin"), "r") as f:
            bytecode = f.read().strip()
        
        return abi, bytecode
    except FileNotFoundError:
        # Placeholder ABI and bytecode for development
        # In production, these should be properly compiled from the Solidity file
        print(f"Warning: Contract files for {contract_name} not found. Using placeholder data.")
        return [], "0x"


def deploy_rental_agreement(tenant_address, property_id, start_date, end_date, monthly_rent):
    """Deploy a new RentalAgreement contract to the blockchain"""
    try:
        # Load contract ABI and bytecode
        abi, bytecode = load_contract_data("RentalAgreement")
        
        # Create contract
        RentalAgreement = w3.eth.contract(abi=abi, bytecode=bytecode)
        
        # Build transaction
        construct_txn = RentalAgreement.constructor(
            tenant_address,
            property_id,
            start_date,
            end_date,
            monthly_rent
        ).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price
        })
        
        # Sign transaction
        signed = account.sign_transaction(construct_txn)
        
        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        
        # Wait for transaction to be mined
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            'contract_address': tx_receipt.contractAddress,
            'tx_hash': tx_hash.hex(),
            'block_number': tx_receipt.blockNumber
        }
    except Exception as e:
        print(f"Error deploying contract: {e}")
        raise


def get_agreement_details(contract_address):
    """Get details of an existing rental agreement"""
    try:
        # Load contract ABI
        abi, _ = load_contract_data("RentalAgreement")
        
        # Create contract instance
        contract = w3.eth.contract(address=contract_address, abi=abi)
        
        # Call getAgreementDetails function
        details = contract.functions.getAgreementDetails().call()
        
        # Format details
        return {
            'landlord': details[0],
            'tenant': details[1],
            'property_id': details[2],
            'start_date': details[3],
            'end_date': details[4],
            'monthly_rent': details[5],
            'security_deposit': details[6],
            'status': details[7],
            'security_deposit_returned': details[8]
        }
    except Exception as e:
        print(f"Error getting agreement details: {e}")
        raise


def terminate_agreement(contract_address):
    """Terminate a rental agreement"""
    try:
        # Load contract ABI
        abi, _ = load_contract_data("RentalAgreement")
        
        # Create contract instance
        contract = w3.eth.contract(address=contract_address, abi=abi)
        
        # Build transaction
        txn = contract.functions.terminateAgreement().build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })
        
        # Sign transaction
        signed = account.sign_transaction(txn)
        
        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        
        # Wait for transaction to be mined
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            'tx_hash': tx_hash.hex(),
            'block_number': tx_receipt.blockNumber,
            'status': tx_receipt.status
        }
    except Exception as e:
        print(f"Error terminating agreement: {e}")
        raise


def complete_agreement(contract_address):
    """Mark a rental agreement as completed"""
    try:
        # Load contract ABI
        abi, _ = load_contract_data("RentalAgreement")
        
        # Create contract instance
        contract = w3.eth.contract(address=contract_address, abi=abi)
        
        # Build transaction
        txn = contract.functions.completeAgreement().build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })
        
        # Sign transaction
        signed = account.sign_transaction(txn)
        
        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        
        # Wait for transaction to be mined
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            'tx_hash': tx_hash.hex(),
            'block_number': tx_receipt.blockNumber,
            'status': tx_receipt.status
        }
    except Exception as e:
        print(f"Error completing agreement: {e}")
        raise 