from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from ..database import get_db
from ..blockchain.contract_service import contract_service
from .auth import get_current_active_user
from .. import models, schemas

router = APIRouter()

# Blockchain Status Models
class BlockchainStatus(BaseModel):
    is_connected: bool
    network_name: str
    block_number: int
    contract_addresses: Dict[str, Optional[str]]

# Blockchain Agreement Models
class BlockchainAgreementCreate(BaseModel):
    property_id: str
    landlord_address: str
    start_date: datetime
    end_date: datetime
    monthly_rent: float
    security_deposit: float

class BlockchainAgreementResponse(BaseModel):
    success: bool
    transaction_hash: Optional[str] = None
    agreement_id: Optional[int] = None
    block_number: Optional[int] = None
    error: Optional[str] = None

class WalletSignatureVerification(BaseModel):
    message: str
    signature: str
    address: str

# Routes

@router.get("/blockchain/status", response_model=BlockchainStatus)
async def get_blockchain_status():
    """Get current blockchain network status"""
    is_connected = contract_service.is_connected()
    
    if not is_connected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain network connection is unavailable"
        )
    
    block_number = contract_service.get_block_number()
    network_name = contract_service._get_network_name()
    
    return {
        "is_connected": is_connected,
        "network_name": network_name,
        "block_number": block_number,
        "contract_addresses": {
            "rental_contract": contract_service.rental_contract_address
        }
    }

@router.post("/blockchain/agreements", response_model=BlockchainAgreementResponse)
async def create_blockchain_agreement(
    agreement_data: BlockchainAgreementCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new rental agreement on the blockchain"""
    # Check if the contract service is initialized
    if not contract_service.is_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain network connection is unavailable"
        )
    
    # Convert dates to Unix timestamps
    start_timestamp = int(agreement_data.start_date.timestamp())
    end_timestamp = int(agreement_data.end_date.timestamp())
    
    # Call the contract service
    result = contract_service.create_rental_agreement(
        property_id=agreement_data.property_id,
        landlord_address=agreement_data.landlord_address,
        start_date=start_timestamp,
        end_date=end_timestamp,
        monthly_rent=agreement_data.monthly_rent,
        security_deposit=agreement_data.security_deposit
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create blockchain agreement: {result.get('error', 'Unknown error')}"
        )
    
    # If successful, store blockchain reference in database
    # Create a database record linking to the blockchain agreement
    blockchain_ref = models.BlockchainReference(
        user_id=current_user.id,
        transaction_hash=result["transaction_hash"],
        agreement_id=result.get("agreement_id"),
        property_id=agreement_data.property_id,
        block_number=result.get("block_number")
    )
    
    db.add(blockchain_ref)
    db.commit()
    db.refresh(blockchain_ref)
    
    return result

@router.get("/blockchain/agreements/{agreement_id}")
async def get_blockchain_agreement(
    agreement_id: int,
    current_user: models.User = Depends(get_current_active_user)
):
    """Get a rental agreement from the blockchain by ID"""
    if not contract_service.is_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain network connection is unavailable"
        )
    
    result = contract_service.get_rental_agreement(agreement_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agreement not found or error: {result.get('error', 'Unknown error')}"
        )
    
    return result

@router.get("/blockchain/tenant/{address}/agreements")
async def get_tenant_blockchain_agreements(
    address: str,
    current_user: models.User = Depends(get_current_active_user)
):
    """Get all blockchain agreements for a tenant"""
    if not contract_service.is_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain network connection is unavailable"
        )
    
    result = contract_service.get_tenant_agreements(address)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get agreements: {result.get('error', 'Unknown error')}"
        )
    
    return result

@router.get("/blockchain/landlord/{address}/agreements")
async def get_landlord_blockchain_agreements(
    address: str,
    current_user: models.User = Depends(get_current_active_user)
):
    """Get all blockchain agreements for a landlord"""
    if not contract_service.is_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain network connection is unavailable"
        )
    
    result = contract_service.get_landlord_agreements(address)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get agreements: {result.get('error', 'Unknown error')}"
        )
    
    return result

@router.post("/blockchain/verify-signature")
async def verify_wallet_signature(verification_data: WalletSignatureVerification):
    """Verify a message signature from a wallet"""
    if not contract_service.is_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain network connection is unavailable"
        )
    
    is_valid = contract_service.verify_signature(
        message=verification_data.message,
        signature=verification_data.signature,
        address=verification_data.address
    )
    
    return {
        "success": True,
        "is_valid": is_valid
    }

@router.get("/blockchain/balance/{address}")
async def get_wallet_balance(
    address: str,
    current_user: models.User = Depends(get_current_active_user)
):
    """Get the ETH balance of a wallet address"""
    if not contract_service.is_connected():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain network connection is unavailable"
        )
    
    balance = contract_service.get_address_balance(address)
    
    return {
        "success": True,
        "address": address,
        "balance": balance,
        "currency": "ETH"
    } 