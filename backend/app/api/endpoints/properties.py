from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Property, User
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertyResponse
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/properties", response_model=List[PropertyResponse])
async def list_properties(
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    bedrooms: Optional[int] = None,
    city: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all properties with optional filtering
    """
    query = db.query(Property)
    
    if min_price is not None:
        query = query.filter(Property.price >= min_price)
    if max_price is not None:
        query = query.filter(Property.price <= max_price)
    if bedrooms is not None:
        query = query.filter(Property.bedrooms == bedrooms)
    if city is not None:
        query = query.filter(Property.address['city'].astext == city)
    if status is not None:
        query = query.filter(Property.status == status)
        
    properties = query.all()
    return properties

@router.post("/properties", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_data: PropertyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new property listing
    """
    if current_user.role not in ['landlord', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only landlords can create property listings"
        )
        
    new_property = Property(
        **property_data.dict(),
        owner_id=current_user.id,
        status="available"
    )
    
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    
    return new_property

@router.get("/properties/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific property by ID
    """
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    return property

@router.patch("/properties/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: str,
    property_data: PropertyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a property listing
    """
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
        
    if property.owner_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this property"
        )
    
    # Update only the fields provided
    for key, value in property_data.dict(exclude_unset=True).items():
        setattr(property, key, value)
        
    db.commit()
    db.refresh(property)
    
    return property

@router.delete("/properties/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a property listing
    """
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
        
    if property.owner_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this property"
        )
    
    # Check if property is listed on blockchain before deletion
    if property.blockchain_id:
        # You may want to add blockchain unlisting logic here
        pass
    
    db.delete(property)
    db.commit()
    
    return None 