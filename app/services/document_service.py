"""
Document service for database operations.
"""

from typing import Dict, List, Optional, Any, BinaryIO
from datetime import datetime
import base64
import hashlib
import os
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
from app.core.config import settings


class DocumentService:
    """Service for document database operations."""
    
    COLLECTION = "documents"
    
    @classmethod
    async def create_document(cls, document_data: Dict, file_data: Optional[bytes] = None) -> str:
        """Create a new document."""
        # Set default document type
        if "document_type" not in document_data:
            document_data["document_type"] = "other"
        
        # Generate document hash if file data is provided
        if file_data:
            document_data["document_hash"] = cls._generate_document_hash(file_data)
            
            # Store file data if required
            if settings.STORE_DOCUMENTS_IN_DB:
                document_data["document_data"] = file_data
        
        # Store blockchain transaction ID if available
        if "blockchain_tx_id" not in document_data:
            document_data["blockchain_tx_id"] = None
        
        # Create document in MongoDB
        document_id = await create_document(cls.COLLECTION, document_data)
        return document_id
    
    @classmethod
    async def get_document(cls, document_id: str) -> Optional[Dict]:
        """Get a document by ID."""
        return await get_document(cls.COLLECTION, document_id)
    
    @classmethod
    async def update_document(cls, document_id: str, update_data: Dict) -> bool:
        """Update a document by ID."""
        return await update_document(cls.COLLECTION, document_id, update_data)
    
    @classmethod
    async def delete_document(cls, document_id: str) -> bool:
        """Delete a document by ID."""
        return await delete_document(cls.COLLECTION, document_id)
    
    @classmethod
    async def list_documents(
        cls,
        filter_query: Dict = None,
        skip: int = 0,
        limit: int = 20,
        sort: List = None
    ) -> List[Dict]:
        """List documents with pagination and filtering."""
        return await list_documents(
            cls.COLLECTION,
            filter_query=filter_query,
            skip=skip,
            limit=limit,
            sort=sort
        )
    
    @classmethod
    async def get_documents_by_user(cls, user_id: str) -> List[Dict]:
        """Get documents for a specific user."""
        return await list_documents(
            cls.COLLECTION,
            filter_query={"user_id": user_id},
            sort=[("created_at", -1)]
        )
    
    @classmethod
    async def get_documents_by_property(cls, property_id: str) -> List[Dict]:
        """Get documents for a specific property."""
        return await list_documents(
            cls.COLLECTION,
            filter_query={"property_id": property_id},
            sort=[("created_at", -1)]
        )
    
    @classmethod
    async def get_documents_by_contract(cls, contract_id: str) -> List[Dict]:
        """Get documents for a specific contract."""
        return await list_documents(
            cls.COLLECTION,
            filter_query={"contract_id": contract_id},
            sort=[("created_at", -1)]
        )
    
    @classmethod
    async def get_document_by_hash(cls, document_hash: str) -> Optional[Dict]:
        """Get a document by its hash."""
        collection = await get_collection(cls.COLLECTION)
        document = await collection.find_one({"document_hash": document_hash})
        return format_document_for_response(document) if document else None
    
    @classmethod
    async def store_document_file(cls, document_id: str, file_data: bytes) -> bool:
        """Store file data for an existing document."""
        document_hash = cls._generate_document_hash(file_data)
        
        update_data = {
            "document_hash": document_hash
        }
        
        # Store file data if required
        if settings.STORE_DOCUMENTS_IN_DB:
            update_data["document_data"] = file_data
            
        return await update_document(cls.COLLECTION, document_id, update_data)
    
    @classmethod
    async def get_document_file(cls, document_id: str) -> Optional[bytes]:
        """Get file data for a document."""
        document = await cls.get_document(document_id)
        
        if not document:
            return None
            
        # If file data is stored in database
        if "document_data" in document and document["document_data"]:
            return document["document_data"]
            
        # If file is stored on filesystem
        if "document_url" in document and document["document_url"]:
            file_path = document["document_url"]
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    return f.read()
                    
        return None
    
    @classmethod
    async def update_blockchain_reference(cls, document_id: str, blockchain_tx_id: str) -> bool:
        """Update the blockchain reference for a document."""
        return await update_document(
            cls.COLLECTION,
            document_id,
            {"blockchain_tx_id": blockchain_tx_id}
        )
    
    @staticmethod
    def _generate_document_hash(file_data: bytes) -> str:
        """Generate a unique hash for a document."""
        return hashlib.sha256(file_data).hexdigest()
    
    @classmethod
    async def verify_document_hash(cls, document_id: str, file_data: bytes) -> bool:
        """Verify if a document's hash matches the stored hash."""
        document = await cls.get_document(document_id)
        
        if not document or "document_hash" not in document:
            return False
            
        calculated_hash = cls._generate_document_hash(file_data)
        return calculated_hash == document["document_hash"] 