"""
Hyperledger Fabric service implementation for SmartRent platform.
Handles all Hyperledger Fabric interactions.
"""
from typing import Dict, Optional, List
from hfc.fabric import Client
import asyncio
import logging
import json

logger = logging.getLogger(__name__)

class HyperledgerService:
    """Manages Hyperledger Fabric operations."""
    
    def __init__(self, network_config: Dict):
        """Initialize Hyperledger Fabric client with network configuration."""
        self.client = Client(net_profile=network_config)
        self.channel_name = network_config.get('channel_name', 'mychannel')
        self.chaincode_name = network_config.get('chaincode_name', 'smartrent')
        
    async def connect(self) -> bool:
        """Establish connection to Hyperledger Fabric network."""
        try:
            # Initialize the channel
            await self.client.init_with_discovery(self.channel_name)
            logger.info(f"Connected to Hyperledger Fabric channel: {self.channel_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Hyperledger Fabric: {e}")
            return False
            
    async def record_transaction(
        self, 
        transaction_data: Dict,
        solana_ref: str
    ) -> Dict:
        """Record a transaction in Hyperledger Fabric."""
        try:
            # Prepare transaction data
            payload = {
                'solanaRef': solana_ref,
                'timestamp': transaction_data.get('timestamp'),
                'data': transaction_data
            }
            
            # Submit transaction to chaincode
            response = await self.client.chaincode_invoke(
                requestor=self.client.get_user('admin'),
                channel_name=self.channel_name,
                peers=['peer0.org1.example.com'],
                args=[json.dumps(payload)],
                cc_name=self.chaincode_name,
                fcn='recordTransaction'
            )
            
            return {
                'success': True,
                'fabric_id': response.transaction_id,
                'timestamp': response.timestamp
            }
        except Exception as e:
            logger.error(f"Failed to record transaction: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    async def query_transaction(self, fabric_id: str) -> Dict:
        """Query a transaction from Hyperledger Fabric."""
        try:
            response = await self.client.chaincode_query(
                requestor=self.client.get_user('admin'),
                channel_name=self.channel_name,
                peers=['peer0.org1.example.com'],
                args=[fabric_id],
                cc_name=self.chaincode_name,
                fcn='queryTransaction'
            )
            
            return {
                'success': True,
                'data': json.loads(response)
            }
        except Exception as e:
            logger.error(f"Failed to query transaction: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    async def update_contract_state(
        self, 
        contract_id: str, 
        new_state: Dict
    ) -> Dict:
        """Update contract state in Hyperledger Fabric."""
        try:
            payload = {
                'contractId': contract_id,
                'newState': new_state,
                'timestamp': new_state.get('timestamp')
            }
            
            response = await self.client.chaincode_invoke(
                requestor=self.client.get_user('admin'),
                channel_name=self.channel_name,
                peers=['peer0.org1.example.com'],
                args=[json.dumps(payload)],
                cc_name=self.chaincode_name,
                fcn='updateContractState'
            )
            
            return {
                'success': True,
                'transaction_id': response.transaction_id
            }
        except Exception as e:
            logger.error(f"Failed to update contract state: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    async def get_contract_history(
        self, 
        contract_id: str
    ) -> List[Dict]:
        """Get the history of a contract from Hyperledger Fabric."""
        try:
            response = await self.client.chaincode_query(
                requestor=self.client.get_user('admin'),
                channel_name=self.channel_name,
                peers=['peer0.org1.example.com'],
                args=[contract_id],
                cc_name=self.chaincode_name,
                fcn='getContractHistory'
            )
            
            return {
                'success': True,
                'history': json.loads(response)
            }
        except Exception as e:
            logger.error(f"Failed to get contract history: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def close(self):
        """Close the Hyperledger Fabric client connection."""
        try:
            self.client.close()
        except Exception as e:
            logger.error(f"Error closing Hyperledger connection: {e}") 