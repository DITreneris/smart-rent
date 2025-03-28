from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models
from ..database import get_db
from ..schemas import contracts as contract_schemas
from .auth import get_current_active_user

router = APIRouter()


@router.post("/contracts", response_model=contract_schemas.ContractResponse)
async def create_contract(
    contract_data: contract_schemas.ContractCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    # Verify that property exists and is available
    property_item = db.query(models.Property).filter(models.Property.id == contract_data.property_id).first()
    if not property_item:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if property_item.status != models.PropertyStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Property is not available for rent")
    
    # Only tenants can initiate contracts
    if current_user.role != models.UserRole.TENANT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only tenants can request rental contracts",
        )
    
    # Create the contract
    new_contract = models.Contract(
        property_id=contract_data.property_id,
        tenant_id=current_user.id,
        landlord_id=property_item.owner_id,
        start_date=contract_data.start_date,
        end_date=contract_data.end_date,
        monthly_rent=contract_data.monthly_rent,
        security_deposit=contract_data.security_deposit,
        status=models.ContractStatus.PENDING,
    )
    
    # Update property status to pending contract
    property_item.status = models.PropertyStatus.PENDING
    
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    
    return new_contract


@router.get("/contracts", response_model=List[contract_schemas.ContractResponse])
async def list_contracts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    # Filter contracts based on user role
    if current_user.role == models.UserRole.TENANT:
        return db.query(models.Contract).filter(models.Contract.tenant_id == current_user.id).all()
    elif current_user.role == models.UserRole.LANDLORD:
        return db.query(models.Contract).filter(models.Contract.landlord_id == current_user.id).all()
    elif current_user.role == models.UserRole.ADMIN:
        return db.query(models.Contract).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized",
        )


@router.get("/contracts/{contract_id}", response_model=contract_schemas.ContractResponse)
async def get_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    contract = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Check if user is authorized to view this contract
    if (current_user.role == models.UserRole.TENANT and contract.tenant_id != current_user.id) or \
       (current_user.role == models.UserRole.LANDLORD and contract.landlord_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this contract",
        )
    
    return contract


@router.put("/contracts/{contract_id}/confirm", response_model=contract_schemas.ContractResponse)
async def confirm_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    contract = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Only landlord can confirm a contract
    if current_user.role != models.UserRole.LANDLORD or contract.landlord_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the landlord can confirm this contract",
        )
    
    if contract.status != models.ContractStatus.PENDING:
        raise HTTPException(status_code=400, detail="Contract is not in pending status")
    
    # Update contract status to active
    contract.status = models.ContractStatus.ACTIVE
    
    # Update property status to rented
    property_item = db.query(models.Property).filter(models.Property.id == contract.property_id).first()
    if property_item:
        property_item.status = models.PropertyStatus.RENTED
    
    db.commit()
    db.refresh(contract)
    
    return contract


@router.put("/contracts/{contract_id}/cancel", response_model=contract_schemas.ContractResponse)
async def cancel_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    contract = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Check if user is authorized to cancel this contract
    if (current_user.role == models.UserRole.TENANT and contract.tenant_id != current_user.id) or \
       (current_user.role == models.UserRole.LANDLORD and contract.landlord_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this contract",
        )
    
    if contract.status not in [models.ContractStatus.PENDING, models.ContractStatus.ACTIVE]:
        raise HTTPException(status_code=400, detail="Contract cannot be cancelled in its current state")
    
    # Update contract status to cancelled
    contract.status = models.ContractStatus.CANCELLED
    
    # Update property status to available if it was rented or pending
    property_item = db.query(models.Property).filter(models.Property.id == contract.property_id).first()
    if property_item and property_item.status in [models.PropertyStatus.RENTED, models.PropertyStatus.PENDING]:
        property_item.status = models.PropertyStatus.APPROVED
    
    db.commit()
    db.refresh(contract)
    
    return contract


@router.put("/contracts/{contract_id}/complete", response_model=contract_schemas.ContractResponse)
async def complete_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    contract = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Only landlord can complete a contract
    if current_user.role != models.UserRole.LANDLORD or contract.landlord_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the landlord can complete this contract",
        )
    
    if contract.status != models.ContractStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Contract is not in active status")
    
    # Update contract status to completed
    contract.status = models.ContractStatus.COMPLETED
    
    # Update property status to available
    property_item = db.query(models.Property).filter(models.Property.id == contract.property_id).first()
    if property_item:
        property_item.status = models.PropertyStatus.APPROVED
    
    db.commit()
    db.refresh(contract)
    
    return contract 