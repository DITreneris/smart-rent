"""
Contract service for database operations.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from bson import ObjectId

from app.core.mongo_db import (
    get_collection, 
    create_document, 
    get_document, 
    update_document,
    delete_document,
    list_documents,
    format_document_for_response
)


class ContractService:
    """Service for contract database operations."""
    
    COLLECTION = "contracts"
    
    @classmethod
    async def create_contract(cls, contract_data: Dict) -> str:
        """Create a new rental contract."""
        # Generate a blockchain reference ID if not provided
        if "blockchain_id" not in contract_data:
            contract_data["blockchain_id"] = None
        
        # Set default contract status
        if "status" not in contract_data:
            contract_data["status"] = "draft"
        
        # Create document in MongoDB
        contract_id = await create_document(cls.COLLECTION, contract_data)
        return contract_id
    
    @classmethod
    async def get_contract(cls, contract_id: str) -> Optional[Dict]:
        """Get a contract by ID."""
        return await get_document(cls.COLLECTION, contract_id)
    
    @classmethod
    async def get_contract_by_blockchain_id(cls, blockchain_id: str) -> Optional[Dict]:
        """Get a contract by blockchain ID."""
        collection = await get_collection(cls.COLLECTION)
        document = await collection.find_one({"blockchain_id": blockchain_id})
        return format_document_for_response(document) if document else None
    
    @classmethod
    async def update_contract(cls, contract_id: str, update_data: Dict) -> bool:
        """Update a contract by ID."""
        return await update_document(cls.COLLECTION, contract_id, update_data)
    
    @classmethod
    async def delete_contract(cls, contract_id: str) -> bool:
        """Delete a contract by ID."""
        return await delete_document(cls.COLLECTION, contract_id)
    
    @classmethod
    async def list_contracts(
        cls, 
        filter_query: Dict = None, 
        skip: int = 0, 
        limit: int = 20,
        sort: List = None
    ) -> List[Dict]:
        """List contracts with pagination and filtering."""
        return await list_documents(
            cls.COLLECTION, 
            filter_query=filter_query, 
            skip=skip, 
            limit=limit,
            sort=sort
        )
    
    @classmethod
    async def add_landlord_signature(cls, contract_id: str, signature: str) -> bool:
        """Add landlord signature to contract."""
        return await update_document(
            cls.COLLECTION,
            contract_id,
            {
                "landlord_signature": signature,
                "landlord_signed_at": datetime.utcnow()
            }
        )
    
    @classmethod
    async def add_tenant_signature(cls, contract_id: str, signature: str) -> bool:
        """Add tenant signature to contract."""
        # Update signature
        result = await update_document(
            cls.COLLECTION,
            contract_id,
            {
                "tenant_signature": signature,
                "tenant_signed_at": datetime.utcnow(),
                "status": "signed"
            }
        )
        
        return result
    
    @classmethod
    async def get_contracts_by_property(cls, property_id: str) -> List[Dict]:
        """Get contracts for a specific property."""
        return await list_documents(
            cls.COLLECTION,
            filter_query={"property_id": property_id},
            sort=[("created_at", -1)]
        )
    
    @classmethod
    async def get_contracts_by_landlord(cls, landlord_id: str) -> List[Dict]:
        """Get contracts owned by a specific landlord."""
        return await list_documents(
            cls.COLLECTION,
            filter_query={"landlord_id": landlord_id},
            sort=[("created_at", -1)]
        )
    
    @classmethod
    async def get_contracts_by_tenant(cls, tenant_id: str) -> List[Dict]:
        """Get contracts for a specific tenant."""
        return await list_documents(
            cls.COLLECTION,
            filter_query={"tenant_id": tenant_id},
            sort=[("created_at", -1)]
        )
    
    @classmethod
    async def activate_contract(cls, contract_id: str, blockchain_tx_id: str = None) -> bool:
        """Mark a contract as active after blockchain confirmation."""
        update_data = {
            "status": "active",
            "activated_at": datetime.utcnow()
        }
        
        if blockchain_tx_id:
            update_data["blockchain_tx_id"] = blockchain_tx_id
            
        return await update_document(cls.COLLECTION, contract_id, update_data)
    
    @classmethod
    async def terminate_contract(cls, contract_id: str, reason: str = None) -> bool:
        """Terminate a contract."""
        update_data = {
            "status": "terminated",
            "terminated_at": datetime.utcnow()
        }
        
        if reason:
            update_data["termination_reason"] = reason
            
        return await update_document(cls.COLLECTION, contract_id, update_data) 