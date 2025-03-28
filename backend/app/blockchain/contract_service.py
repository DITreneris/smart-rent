from typing import Dict, Any, Optional, List
import os
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.contract import Contract
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import Address, ChecksumAddress

class ContractService:
    """Service for interacting with Ethereum smart contracts"""
    
    def __init__(self):
        # Initialize Web3 connection
        # Use environment variables for RPC URL and private key
        rpc_url = os.getenv("ETHEREUM_RPC_URL", "http://localhost:8545")
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        # Add middleware for compatibility with some networks like Polygon or BSC
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Load account from private key if provided
        private_key = os.getenv("ETHEREUM_PRIVATE_KEY")
        self.account: Optional[LocalAccount] = None
        if private_key:
            self.account = Account.from_key(private_key)
        
        # Contract addresses
        self.rental_contract_address = os.getenv("RENTAL_CONTRACT_ADDRESS")
        
        # Load contract ABIs
        self._load_contracts()
        
        print(f"ContractService initialized. Connected to network: {self._get_network_name()}")
    
    def _load_contracts(self) -> None:
        """Load contract ABIs and instantiate contract objects"""
        try:
            # Load RentalContract ABI
            with open(os.path.join(os.path.dirname(__file__), "abi/RentalContract.json"), "r") as f:
                rental_contract_data = json.load(f)
            
            # Create contract instances if addresses are provided
            self.rental_contract: Optional[Contract] = None
            if self.rental_contract_address and self.web3.is_address(self.rental_contract_address):
                self.rental_contract = self.web3.eth.contract(
                    address=self.web3.to_checksum_address(self.rental_contract_address),
                    abi=rental_contract_data["abi"]
                )
        except Exception as e:
            print(f"Error loading contract ABIs: {str(e)}")
    
    def _get_network_name(self) -> str:
        """Get the name of the connected Ethereum network"""
        chain_id = self.web3.eth.chain_id
        networks = {
            1: "Ethereum Mainnet",
            5: "Goerli Testnet",
            11155111: "Sepolia Testnet",
            137: "Polygon Mainnet",
            80001: "Mumbai Testnet",
            56: "Binance Smart Chain",
            97: "BSC Testnet",
            42161: "Arbitrum One",
            421613: "Arbitrum Goerli",
        }
        return networks.get(chain_id, f"Unknown Network (Chain ID: {chain_id})")
    
    def is_connected(self) -> bool:
        """Check if connected to Ethereum network"""
        return self.web3.is_connected()
    
    def get_block_number(self) -> int:
        """Get current block number"""
        return self.web3.eth.block_number
    
    def get_address_balance(self, address: str) -> float:
        """Get ETH balance of an address"""
        try:
            balance_wei = self.web3.eth.get_balance(self.web3.to_checksum_address(address))
            return self.web3.from_wei(balance_wei, "ether")
        except Exception as e:
            print(f"Error getting balance for {address}: {str(e)}")
            return 0
    
    # Rental Contract Methods
    
    def create_rental_agreement(
        self,
        property_id: str,
        landlord_address: str,
        start_date: int,
        end_date: int,
        monthly_rent: int,
        security_deposit: int
    ) -> Dict[str, Any]:
        """Create a new rental agreement on the blockchain"""
        if not self.rental_contract or not self.account:
            return {"success": False, "error": "Contract or account not initialized"}
        
        try:
            # Convert addresses to checksum format
            landlord_address = self.web3.to_checksum_address(landlord_address)
            
            # Convert values to Wei
            monthly_rent_wei = self.web3.to_wei(monthly_rent, "ether")
            security_deposit_wei = self.web3.to_wei(security_deposit, "ether")
            
            # Build the transaction
            tx = self.rental_contract.functions.createAgreement(
                property_id,
                landlord_address,
                start_date,
                end_date,
                monthly_rent_wei,
                security_deposit_wei
            ).build_transaction({
                "from": self.account.address,
                "nonce": self.web3.eth.get_transaction_count(self.account.address),
                "gas": 500000,  # Adjust gas as needed
                "gasPrice": self.web3.eth.gas_price
            })
            
            # Sign and send transaction
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for transaction receipt
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Extract the agreement ID from the event logs
            agreement_id = None
            for log in receipt.logs:
                try:
                    # Try to find the AgreementCreated event
                    if log["topics"][0].hex() == self.rental_contract.events.AgreementCreated.signature:
                        # Decode the event data
                        decoded_log = self.rental_contract.events.AgreementCreated().process_log(log)
                        agreement_id = decoded_log["args"]["agreementId"]
                        break
                except Exception:
                    continue
            
            return {
                "success": True,
                "transaction_hash": receipt.transactionHash.hex(),
                "agreement_id": agreement_id,
                "block_number": receipt.blockNumber
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_rental_agreement(self, agreement_id: int) -> Dict[str, Any]:
        """Get rental agreement details from the blockchain"""
        if not self.rental_contract:
            return {"success": False, "error": "Contract not initialized"}
        
        try:
            # Call the contract method
            agreement = self.rental_contract.functions.getAgreement(agreement_id).call()
            
            # Convert Wei values to ETH
            monthly_rent_eth = self.web3.from_wei(agreement[5], "ether")
            security_deposit_eth = self.web3.from_wei(agreement[6], "ether")
            
            # Format the data
            return {
                "success": True,
                "agreement": {
                    "id": agreement_id,
                    "property_id": agreement[0],
                    "tenant": agreement[1],
                    "landlord": agreement[2],
                    "start_date": agreement[3],
                    "end_date": agreement[4],
                    "monthly_rent": monthly_rent_eth,
                    "security_deposit": security_deposit_eth,
                    "last_payment_date": agreement[7],
                    "status": agreement[8]
                }
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_tenant_agreements(self, tenant_address: str) -> Dict[str, Any]:
        """Get all agreements for a tenant"""
        if not self.rental_contract:
            return {"success": False, "error": "Contract not initialized"}
        
        try:
            # Convert address to checksum format
            tenant_address = self.web3.to_checksum_address(tenant_address)
            
            # Call the contract method
            agreement_ids = self.rental_contract.functions.getAgreementsByTenant(tenant_address).call()
            
            agreements = []
            for agreement_id in agreement_ids:
                agreement_data = self.get_rental_agreement(agreement_id)
                if agreement_data["success"]:
                    agreements.append(agreement_data["agreement"])
            
            return {
                "success": True,
                "agreements": agreements
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_landlord_agreements(self, landlord_address: str) -> Dict[str, Any]:
        """Get all agreements for a landlord"""
        if not self.rental_contract:
            return {"success": False, "error": "Contract not initialized"}
        
        try:
            # Convert address to checksum format
            landlord_address = self.web3.to_checksum_address(landlord_address)
            
            # Call the contract method
            agreement_ids = self.rental_contract.functions.getAgreementsByLandlord(landlord_address).call()
            
            agreements = []
            for agreement_id in agreement_ids:
                agreement_data = self.get_rental_agreement(agreement_id)
                if agreement_data["success"]:
                    agreements.append(agreement_data["agreement"])
            
            return {
                "success": True,
                "agreements": agreements
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def verify_signature(self, message: str, signature: str, address: str) -> bool:
        """Verify that a message was signed by the owner of an address"""
        try:
            # Convert address to checksum format
            address = self.web3.to_checksum_address(address)
            
            # Recover the address from the signature
            recovered_address = Account.recover_message(
                Account.encode_defunct(text=message),
                signature=signature
            )
            
            # Compare with the expected address
            return recovered_address.lower() == address.lower()
        
        except Exception as e:
            print(f"Error verifying signature: {str(e)}")
            return False

# Singleton instance
contract_service = ContractService() 