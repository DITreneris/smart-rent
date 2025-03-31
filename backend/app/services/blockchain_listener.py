import asyncio
from web3 import Web3
from web3.middleware import geth_poa_middleware
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import Property, Rental
from app.core.config import settings
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("blockchain_listener")

# Load contract ABI
with open(settings.CONTRACT_ABI_PATH) as f:
    contract_abi = json.load(f)

class BlockchainListener:
    def __init__(self):
        # Connect to Ethereum node
        self.w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URI))
        
        # Add middleware for POA chains like Polygon or BSC if needed
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Initialize contract
        self.contract = self.w3.eth.contract(
            address=settings.CONTRACT_ADDRESS,
            abi=contract_abi
        )
        
        logger.info(f"Connected to blockchain: {self.w3.is_connected()}")
        logger.info(f"Current block: {self.w3.eth.block_number}")

    async def start_listening(self):
        """
        Start listening for blockchain events
        """
        logger.info("Starting blockchain event listeners")
        
        # Create event filters
        property_filter = self.contract.events.PropertyListed.create_filter(fromBlock='latest')
        rental_filter = self.contract.events.PropertyRented.create_filter(fromBlock='latest')
        
        while True:
            try:
                # Check for new events
                for event in property_filter.get_new_entries():
                    await self.handle_property_listed_event(event)
                    
                for event in rental_filter.get_new_entries():
                    await self.handle_property_rented_event(event)
                    
                # Wait before checking again
                await asyncio.sleep(settings.BLOCKCHAIN_POLLING_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in blockchain listener: {e}")
                await asyncio.sleep(10)  # Wait before retrying
    
    async def handle_property_listed_event(self, event):
        """
        Handle PropertyListed event from blockchain
        """
        logger.info(f"Property listed event: {event}")
        
        try:
            # Extract event data
            property_id = event['args']['propertyId']
            owner = event['args']['owner']
            price = self.w3.from_wei(event['args']['pricePerMonth'], 'ether')
            
            # Get DB session
            db = SessionLocal()
            
            try:
                # Find property by metadata URI if it exists
                property = db.query(Property).filter(
                    Property.blockchain_id == str(property_id)
                ).first()
                
                if property:
                    # Update existing property
                    property.blockchain_id = str(property_id)
                    property.price = float(price)
                    db.commit()
                    logger.info(f"Updated property {property.id} with blockchain ID {property_id}")
                else:
                    logger.warning(f"Property with blockchain ID {property_id} not found in database")
                    
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error handling property listed event: {e}")
    
    async def handle_property_rented_event(self, event):
        """
        Handle PropertyRented event from blockchain
        """
        logger.info(f"Property rented event: {event}")
        
        try:
            # Extract event data
            property_id = event['args']['propertyId']
            tenant = event['args']['tenant']
            start_time = event['args']['startTime']
            duration = event['args']['duration']
            
            # Get DB session
            db = SessionLocal()
            
            try:
                # Find property in database
                property = db.query(Property).filter(
                    Property.blockchain_id == str(property_id)
                ).first()
                
                if property:
                    # Update property status
                    property.status = "rented"
                    
                    # Create rental record
                    rental = Rental(
                        property_id=property.id,
                        tenant_address=tenant,
                        start_date=start_time,
                        duration=duration,
                        transaction_hash=event['transactionHash'].hex()
                    )
                    
                    db.add(rental)
                    db.commit()
                    logger.info(f"Created rental record for property {property.id}")
                else:
                    logger.warning(f"Property with blockchain ID {property_id} not found in database")
                    
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error handling property rented event: {e}")

# Entry point to start the service
async def start_blockchain_listener():
    listener = BlockchainListener()
    await listener.start_listening()

if __name__ == "__main__":
    asyncio.run(start_blockchain_listener()) 