"""
Service layer for handling rental proposals.
"""

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import List, Optional
import uuid
from datetime import datetime # Added for date validation
import hashlib # Added for property ID hashing placeholder
import logging

# Assuming models and schemas are defined appropriately
# Adjust imports based on actual project structure
from app.models.proposal import Proposal, ProposalStatus
from app.models.property import Property, PropertyStatus # Assuming PropertyStatus exists
from app.models.user import User # Assuming User model exists
from app.schemas.proposal import ProposalCreate, ProposalUpdateStatus # Adjust schema import
# Import the new Metadata service and schema
from app.models.rental_metadata import RentalMetadataCreate
from app.services.rental_metadata import RentalMetadataService

# Placeholder for BlockchainService - Adjust import
from app.services.blockchain import BlockchainService
# Import settings for API_BASE_URL
from app.core.config import settings
# Placeholder for PropertyService - Adjust import
# from app.services.property import PropertyService

logger = logging.getLogger(__name__)

class ProposalService:
    
    @staticmethod
    async def create_proposal(db: AsyncSession, proposal_in: ProposalCreate, tenant_user: User) -> Proposal:
        """Creates a new rental proposal (Async)."""
        # 1. Validate Property Exists and is Available (Async)
        stmt_prop = select(Property).where(Property.id == proposal_in.property_id)
        result_prop = await db.execute(stmt_prop)
        property_db = result_prop.scalars().first()
        
        if not property_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
        if property_db.status != PropertyStatus.AVAILABLE.value: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Property is not available")
        
        # 2. Validate Dates (Sync logic is fine)
        if proposal_in.start_date >= proposal_in.end_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date must be before end date")
        if proposal_in.start_date < datetime.utcnow().date(): 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date cannot be in the past")
        
        # 3. (Optional) Validate Signature (Sync or Async depending on method)
        if proposal_in.tenant_signature:
            is_signature_valid = True # Replace with actual check (can be async)
            if not is_signature_valid:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid tenant signature")
        
        # 4. Create Proposal DB Object (Sync object creation)
        proposal_db = Proposal(
            property_id=proposal_in.property_id,
            start_date=proposal_in.start_date,
            end_date=proposal_in.end_date,
            price_offer=proposal_in.price_offer,
            message=proposal_in.message,
            tenant_signature=proposal_in.tenant_signature, 
            tenant_id=tenant_user.id,
            status=ProposalStatus.PENDING.value 
        )
        db.add(proposal_db)
        try:
            await db.commit() # Async commit
            await db.refresh(proposal_db) # Async refresh
        except Exception as e:
            await db.rollback() # Async rollback
            # Log the error e
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create proposal.")
        
        return proposal_db

    @staticmethod
    async def get_proposal_by_id(db: AsyncSession, proposal_id: str) -> Optional[Proposal]:
        """Retrieves a proposal by its ID (Async)."""
        stmt = select(Proposal).where(Proposal.id == proposal_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_proposals_for_tenant(db: AsyncSession, tenant_user: User) -> List[Proposal]:
        """Retrieves all proposals submitted by a specific tenant (Async)."""
        stmt = select(Proposal).where(Proposal.tenant_id == tenant_user.id).order_by(Proposal.created_at.desc())
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_proposals_for_landlord(db: AsyncSession, landlord_user: User) -> List[Proposal]:
        """Retrieves all proposals for properties owned by a specific landlord (Async)."""
        stmt = select(Proposal).join(Property, Proposal.property_id == Property.id).where(Property.owner_id == landlord_user.id).order_by(Proposal.created_at.desc())
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_proposal_status(db: AsyncSession, proposal_id: str, new_status: ProposalStatus, current_user: User) -> Proposal:
        """Updates the status of a proposal (accept, reject, cancel) (Async)."""
        # Fetch proposal async
        proposal_db = await ProposalService.get_proposal_by_id(db, proposal_id)
        if not proposal_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")
        
        # Permission Checks (Sync logic is fine, assuming relationships are loaded or accessed synchronously)
        # Note: Accessing relationships like proposal_db.property might trigger lazy loading.
        # For async, explicit loading might be needed if not configured for eager loading.
        # Let's assume for now relationships are accessible after initial load.
        if not hasattr(proposal_db, 'property') or not proposal_db.property or not hasattr(proposal_db.property, 'owner_id'):
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Proposal data incomplete")
             
        is_landlord = proposal_db.property.owner_id == current_user.id
        is_tenant = proposal_db.tenant_id == current_user.id
        original_status = proposal_db.status
        
        allowed_transition = False 
        # (Permission/Transition logic remains synchronous) ...
        # Landlord Actions
        if is_landlord and new_status in [ProposalStatus.ACCEPTED, ProposalStatus.REJECTED]:
            if original_status == ProposalStatus.PENDING.value:
                allowed_transition = True
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot {new_status.value} proposal from status {original_status}")
        
        # Tenant Actions
        elif is_tenant and new_status == ProposalStatus.CANCELLED:
             if original_status == ProposalStatus.PENDING.value:
                 allowed_transition = True
             else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot cancel proposal from status {original_status}")
                
        # Check Permissions
        if not allowed_transition:
             if not (is_landlord or is_tenant):
                 raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized for this proposal")
             else: 
                  raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted for user role or proposal status")

        # Update status (Sync)
        proposal_db.status = new_status.value 
            
        try:
            await db.commit() # Async commit
            await db.refresh(proposal_db) # Async refresh
        except Exception as e:
            await db.rollback() # Async rollback
            # Log error e
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update proposal status.")
            
        return proposal_db

    @staticmethod
    async def trigger_onchain_confirmation(db: AsyncSession, proposal_id: str, current_user: User) -> Proposal:
        """Orchestrates the on-chain confirmation step (Async)."""
        # Fetch proposal async
        proposal_db = await ProposalService.get_proposal_by_id(db, proposal_id)
        if not proposal_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")

        # --- Permission & Status Checks (Sync logic is fine after async fetch) ---
        if not hasattr(proposal_db, 'property') or not proposal_db.property or not hasattr(proposal_db.property, 'owner_id'):
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Proposal property data incomplete.")
        if not hasattr(proposal_db, 'tenant'):
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Proposal tenant data incomplete.")

        if proposal_db.property.owner_id != current_user.id:
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the property owner can confirm the rental")

        if proposal_db.status != ProposalStatus.ACCEPTED.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only accepted proposals can be confirmed")
        # --------------------------------

        # --- Metadata Preparation (Sync logic fine) ---
        metadata_dict = {
            "schema": "urn:smartrent:rental-metadata:v1.0", 
            "proposalId": proposal_db.id,
            "propertyId": proposal_db.property_id,
            "tenantId": proposal_db.tenant_id,
            "landlordId": proposal_db.property.owner_id,
            "tenantWallet": getattr(proposal_db.tenant, 'wallet_address', 'N/A'),
            "landlordWallet": getattr(proposal_db.property.owner, 'wallet_address', 'N/A'), 
            "startDate": proposal_db.start_date.isoformat(),
            "endDate": proposal_db.end_date.isoformat(),
            "priceOffer": float(proposal_db.price_offer),
            "message": proposal_db.message,
            "acceptedAt": proposal_db.updated_at.isoformat(), 
            "confirmedAt": datetime.utcnow().isoformat()
        }

        # --- Metadata Storage --- 
        # Assuming RentalMetadataService.create_metadata is now async
        try:
             metadata_create_schema = RentalMetadataCreate(data=metadata_dict)
             # IMPORTANT: We need to refactor RentalMetadataService to be async as well
             metadata_record = await RentalMetadataService.create_metadata(db=db, metadata_in=metadata_create_schema)
             metadata_uri = f"{settings.API_BASE_URL}{settings.API_V1_PREFIX}/metadata/rentals/{metadata_record.id}"
        except Exception as e:
             # Rollback might be needed if create_metadata committed separately
             # await db.rollback() 
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to store rental metadata: {e}")
        # ----------------------

        # --- Wallet Address Retrieval (Needs Async Fetch) ---
        tenant_user = getattr(proposal_db, 'tenant', None)
        landlord_user = getattr(proposal_db.property, 'owner', None)
        
        if not tenant_user:
             stmt_tenant = select(User).where(User.id == proposal_db.tenant_id)
             result_tenant = await db.execute(stmt_tenant)
             tenant_user = result_tenant.scalars().first()
        if not landlord_user:
             stmt_landlord = select(User).where(User.id == proposal_db.property.owner_id)
             result_landlord = await db.execute(stmt_landlord)
             landlord_user = result_landlord.scalars().first()
        
        tenant_wallet_address = getattr(tenant_user, 'wallet_address', None)
        landlord_wallet_address = getattr(landlord_user, 'wallet_address', None)
        
        if not tenant_wallet_address:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Wallet address not found for tenant {proposal_db.tenant_id}")
        if not landlord_wallet_address:
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Wallet address not found for landlord {proposal_db.property.owner_id}")
        # ------------------------------------------

        # --- Rental ID Conversion ---
        # Convert proposal UUID string to bytes32 for Solidity contract.
        try:
            # Hash the UUID string and take the digest (32 bytes)
            rental_id_bytes = hashlib.sha256(proposal_db.id.encode()).digest()
            if len(rental_id_bytes) != 32:
                 # This shouldn't happen with SHA256 digest, but as a safeguard:
                 raise ValueError("SHA256 hash did not produce 32 bytes")
        except ValueError as e:
             logger.error(f"Failed to convert proposal ID {proposal_db.id} to bytes32: {e}")
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid proposal ID format for conversion")
        # ----------------------------------------

        # --- Property ID Conversion ---
        # Convert property UUID string to uint256 for Solidity contract using hashing.
        try:
             property_id_hex = hashlib.sha256(proposal_db.property_id.encode()).hexdigest()
             property_id_int = int(property_id_hex, 16) % (2**256)
        except (ValueError, TypeError, AttributeError) as e:
             logger.error(f"Failed to convert property ID {proposal_db.property_id} to uint256 via hash: {e}")
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid property ID format for conversion")
        # ----------------------------------------

        # Prepare Payload for BlockchainService
        confirm_payload = {
            "rental_id": rental_id_bytes, # bytes32 (from hash)
            "property_id": property_id_int, # uint256 (from hash)
            "tenant_address": tenant_wallet_address, # address
            "landlord_address": landlord_wallet_address, # address
            "metadata_uri": metadata_uri # string
        }

        # Call BlockchainService (Already Async)
        try:
            tx_hash = await BlockchainService.trigger_confirm_rental(payload=confirm_payload)
            if not tx_hash or not tx_hash.startswith('0x'):
                 raise Exception("Blockchain service returned an invalid transaction hash.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Blockchain confirmation transaction failed: {e}")

        # Update Proposal in DB (Needs to call async version)
        updated_proposal = await ProposalService.update_proposal_after_confirmation(
            db=db, 
            proposal_id=proposal_id, 
            tx_hash=tx_hash, 
            metadata_uri=metadata_uri 
        )

        if not updated_proposal:
             print(f"CRITICAL: DB update failed for proposal {proposal_id} after successful tx {tx_hash}.")
             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Proposal confirmed on-chain, but failed to update local status. Please contact support.")

        return updated_proposal

    @staticmethod
    async def update_proposal_after_confirmation(db: AsyncSession, proposal_id: str, tx_hash: str, metadata_uri: str) -> Optional[Proposal]:
        """Updates the proposal record after successful on-chain confirmation (Async)."""
        # Fetch proposal async
        proposal_db = await ProposalService.get_proposal_by_id(db, proposal_id)

        if not proposal_db:
            print(f"Error: Proposal {proposal_id} not found during confirmation update.")
            return None

        # Check status carefully before updating (Sync logic fine)
        if proposal_db.status == ProposalStatus.ACCEPTED.value:
            proposal_db.status = ProposalStatus.CONFIRMED.value
            proposal_db.confirmation_tx_hash = tx_hash
            proposal_db.metadata_uri = metadata_uri 
            try:
                await db.commit() # Async commit
                await db.refresh(proposal_db) # Async refresh
                print(f"Proposal {proposal_id} successfully updated to CONFIRMED.")
                return proposal_db
            except Exception as e:
                 await db.rollback() # Async rollback
                 print(f"CRITICAL ERROR: Failed to commit DB update for proposal {proposal_id} after tx {tx_hash}. Error: {e}")
                 return None 
        elif proposal_db.status == ProposalStatus.CONFIRMED.value:
             print(f"Info: Proposal {proposal_id} was already CONFIRMED. Tx: {tx_hash}")
             return proposal_db
        else:
             print(f"Warning: Proposal {proposal_id} status was {proposal_db.status} when attempting DB confirmation update for tx {tx_hash}. Update skipped.")
             return None 