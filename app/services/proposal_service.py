"""
Proposal service for database operations.
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


class ProposalService:
    """Service for proposal database operations."""
    
    COLLECTION = "proposals"
    
    @classmethod
    async def create_proposal(cls, proposal_data: Dict) -> str:
        """Create a new rental proposal."""
        # Set default status
        if "status" not in proposal_data:
            proposal_data["status"] = "pending"
        
        # Set active flag
        if "is_active" not in proposal_data:
            proposal_data["is_active"] = True
        
        # Store blockchain transaction ID if available
        if "blockchain_tx_id" not in proposal_data:
            proposal_data["blockchain_tx_id"] = None
        
        # Create document in MongoDB
        proposal_id = await create_document(cls.COLLECTION, proposal_data)
        
        # Update property proposal count
        await cls._increment_property_proposal_count(proposal_data["property_id"])
        
        return proposal_id
    
    @classmethod
    async def get_proposal(cls, proposal_id: str) -> Optional[Dict]:
        """Get a proposal by ID."""
        return await get_document(cls.COLLECTION, proposal_id)
    
    @classmethod
    async def update_proposal(cls, proposal_id: str, update_data: Dict) -> bool:
        """Update a proposal by ID."""
        return await update_document(cls.COLLECTION, proposal_id, update_data)
    
    @classmethod
    async def delete_proposal(cls, proposal_id: str) -> bool:
        """Delete a proposal by ID."""
        proposal = await cls.get_proposal(proposal_id)
        if proposal:
            # Update property proposal count
            await cls._decrement_property_proposal_count(proposal["property_id"])
            
        return await delete_document(cls.COLLECTION, proposal_id)
    
    @classmethod
    async def list_proposals(
        cls,
        filter_query: Dict = None,
        skip: int = 0,
        limit: int = 20,
        sort: List = None
    ) -> List[Dict]:
        """List proposals with pagination and filtering."""
        return await list_documents(
            cls.COLLECTION,
            filter_query=filter_query,
            skip=skip,
            limit=limit,
            sort=sort
        )
    
    @classmethod
    async def get_proposals_by_property(cls, property_id: str) -> List[Dict]:
        """Get proposals for a specific property."""
        return await list_documents(
            cls.COLLECTION,
            filter_query={"property_id": property_id, "is_active": True},
            sort=[("price_offer", -1), ("created_at", -1)]
        )
    
    @classmethod
    async def get_proposals_by_tenant(cls, tenant_id: str) -> List[Dict]:
        """Get proposals made by a specific tenant."""
        return await list_documents(
            cls.COLLECTION,
            filter_query={"tenant_id": tenant_id},
            sort=[("created_at", -1)]
        )
    
    @classmethod
    async def accept_proposal(cls, proposal_id: str, contract_id: str = None) -> bool:
        """Accept a proposal and create a contract."""
        update_data = {
            "status": "accepted",
            "accepted_at": datetime.utcnow()
        }
        
        if contract_id:
            update_data["contract_id"] = contract_id
        
        return await update_document(cls.COLLECTION, proposal_id, update_data)
    
    @classmethod
    async def reject_proposal(cls, proposal_id: str, reason: str = None) -> bool:
        """Reject a proposal."""
        update_data = {
            "status": "rejected",
            "rejected_at": datetime.utcnow(),
            "is_active": False
        }
        
        if reason:
            update_data["rejection_reason"] = reason
            
        return await update_document(cls.COLLECTION, proposal_id, update_data)
    
    @classmethod
    async def cancel_proposal(cls, proposal_id: str) -> bool:
        """Cancel a proposal (by tenant)."""
        return await update_document(
            cls.COLLECTION,
            proposal_id,
            {
                "status": "cancelled",
                "cancelled_at": datetime.utcnow(),
                "is_active": False
            }
        )
    
    @classmethod
    async def get_highest_proposal(cls, property_id: str) -> Optional[Dict]:
        """Get the highest price proposal for a property."""
        collection = await get_collection(cls.COLLECTION)
        
        # Find active proposals for this property
        cursor = collection.find({
            "property_id": property_id,
            "is_active": True,
            "status": "pending"
        }).sort("price_offer", -1).limit(1)
        
        proposals = await cursor.to_list(length=1)
        return format_document_for_response(proposals[0]) if proposals else None
    
    @classmethod
    async def update_tenant_signature(cls, proposal_id: str, signature: str) -> bool:
        """Update the tenant signature for a proposal."""
        return await update_document(
            cls.COLLECTION,
            proposal_id,
            {"tenant_signature": signature}
        )
    
    @classmethod
    async def _increment_property_proposal_count(cls, property_id: str) -> None:
        """Increment the proposal count for a property."""
        collection = await get_collection("rental_info")
        
        # Check if rental info exists
        rental_info = await collection.find_one({"property_id": property_id})
        
        if rental_info:
            # Update existing rental info
            await collection.update_one(
                {"property_id": property_id},
                {"$inc": {"number_of_proposals": 1}}
            )
        else:
            # Create new rental info document
            await collection.insert_one({
                "property_id": property_id,
                "number_of_proposals": 1,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
    
    @classmethod
    async def _decrement_property_proposal_count(cls, property_id: str) -> None:
        """Decrement the proposal count for a property."""
        collection = await get_collection("rental_info")
        
        # Update only if rental info exists and count > 0
        await collection.update_one(
            {"property_id": property_id, "number_of_proposals": {"$gt": 0}},
            {"$inc": {"number_of_proposals": -1}}
        ) 