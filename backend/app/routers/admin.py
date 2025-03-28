from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from .. import models
from ..database import get_db
from ..schemas import auth as auth_schemas
from ..schemas import properties as property_schemas
from ..schemas import admin as admin_schemas
from .auth import get_current_active_user

router = APIRouter()


async def get_admin_user(current_user: models.User = Depends(get_current_active_user)):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


@router.get("/admin/pending-users", response_model=List[auth_schemas.UserResponse])
async def get_pending_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user),
):
    return db.query(models.User).filter(models.User.status == models.UserStatus.PENDING).all()


@router.post("/admin/approve-user/{user_id}", response_model=auth_schemas.UserResponse)
async def approve_user(
    user_id: int,
    approval: admin_schemas.UserApproval,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.status != models.UserStatus.PENDING:
        raise HTTPException(status_code=400, detail="User is not in pending status")
    
    user.status = (
        models.UserStatus.APPROVED if approval.approved 
        else models.UserStatus.REJECTED
    )
    
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/admin/pending-properties", response_model=List[property_schemas.PropertyResponse])
async def get_pending_properties(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user),
):
    return db.query(models.Property).filter(models.Property.status == models.PropertyStatus.PENDING).all()


@router.post("/admin/approve-property/{property_id}", response_model=property_schemas.PropertyResponse)
async def approve_property(
    property_id: int,
    approval: admin_schemas.PropertyApproval,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user),
):
    property_item = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not property_item:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if property_item.status != models.PropertyStatus.PENDING:
        raise HTTPException(status_code=400, detail="Property is not in pending status")
    
    property_item.status = (
        models.PropertyStatus.APPROVED if approval.approved 
        else models.PropertyStatus.REJECTED
    )
    
    db.commit()
    db.refresh(property_item)
    
    return property_item


@router.get("/admin/dashboard", response_model=admin_schemas.DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user),
):
    tenant_count = db.query(models.User).filter(
        models.User.role == models.UserRole.TENANT,
        models.User.status == models.UserStatus.APPROVED
    ).count()
    
    landlord_count = db.query(models.User).filter(
        models.User.role == models.UserRole.LANDLORD,
        models.User.status == models.UserStatus.APPROVED
    ).count()
    
    property_stats = {
        "pending": db.query(models.Property).filter(
            models.Property.status == models.PropertyStatus.PENDING
        ).count(),
        "approved": db.query(models.Property).filter(
            models.Property.status == models.PropertyStatus.APPROVED
        ).count(),
        "rejected": db.query(models.Property).filter(
            models.Property.status == models.PropertyStatus.REJECTED
        ).count(),
        "rented": db.query(models.Property).filter(
            models.Property.status == models.PropertyStatus.RENTED
        ).count()
    }
    
    contract_stats = {
        "pending": db.query(models.Contract).filter(
            models.Contract.status == models.ContractStatus.PENDING
        ).count(),
        "active": db.query(models.Contract).filter(
            models.Contract.status == models.ContractStatus.ACTIVE
        ).count(),
        "completed": db.query(models.Contract).filter(
            models.Contract.status == models.ContractStatus.COMPLETED
        ).count(),
        "cancelled": db.query(models.Contract).filter(
            models.Contract.status == models.ContractStatus.CANCELLED
        ).count()
    }
    
    return {
        "tenant_count": tenant_count,
        "landlord_count": landlord_count,
        "pending_approvals": {
            "users": db.query(models.User).filter(
                models.User.status == models.UserStatus.PENDING
            ).count(),
            "properties": property_stats["pending"],
        },
        "property_stats": property_stats,
        "contract_stats": contract_stats
    } 