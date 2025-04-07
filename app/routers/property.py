"""
Property router for property CRUD operations.
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from datetime import datetime

from app.models.property import (
    PropertyResponse,
    PropertyCreateRequest,
    PropertyUpdateRequest,
    PropertySearchResponse,
    PropertySearchFilters,
    PropertyStatus
)
from app.services.property_service import PropertyService
from app.auth.dependencies import get_current_active_user, require_landlord

# Create router
router = APIRouter(
    prefix="/api/properties",
    tags=["properties"],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"}
    }
)

@router.post("", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_data: PropertyCreateRequest,
    current_user: Dict[str, Any] = Depends(require_landlord)
):
    """
    Create a new property listing.
    
    Only landlords can create properties.
    """
    try:
        # Create property
        property_id = await PropertyService.create_property(property_data.dict(), current_user["id"])
        
        # Get created property
        property_data = await PropertyService.get_property(property_id)
        
        if not property_data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create property"
            )
        
        return property_data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create property: {str(e)}"
        )

@router.get("", response_model=PropertySearchResponse)
async def search_properties(
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_bedrooms: Optional[int] = None,
    min_bathrooms: Optional[float] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    available_from: Optional[datetime] = None,
    min_size_sqm: Optional[float] = None,
    status: Optional[str] = PropertyStatus.AVAILABLE,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    Search properties with filters and pagination.
    """
    try:
        # Build filters dictionary
        filters = {
            "property_type": property_type,
            "min_price": min_price,
            "max_price": max_price,
            "min_bedrooms": min_bedrooms,
            "min_bathrooms": min_bathrooms,
            "city": city,
            "state": state,
            "available_from": available_from,
            "min_size_sqm": min_size_sqm,
            "status": status
        }
        
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Search properties
        result = await PropertyService.search_properties(
            filters=filters,
            page=page,
            page_size=page_size
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search properties: {str(e)}"
        )

@router.get("/me", response_model=List[PropertyResponse])
async def get_my_properties(current_user: Dict[str, Any] = Depends(require_landlord)):
    """
    Get properties owned by the current user.
    
    Only landlords can access this endpoint.
    """
    try:
        properties = await PropertyService.get_properties_by_owner(current_user["id"])
        return properties
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get properties: {str(e)}"
        )

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(property_id: str = Path(..., title="Property ID")):
    """
    Get a property by ID.
    """
    property_data = await PropertyService.get_property(property_id)
    
    if not property_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    return property_data

@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_data: PropertyUpdateRequest,
    property_id: str = Path(..., title="Property ID"),
    current_user: Dict[str, Any] = Depends(require_landlord)
):
    """
    Update a property.
    
    Only the property owner can update it.
    """
    # Get property to check ownership
    existing_property = await PropertyService.get_property(property_id)
    
    if not existing_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Check ownership
    if existing_property["owner_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this property"
        )
    
    try:
        # Update property
        success = await PropertyService.update_property(
            property_id,
            property_data.dict(exclude_unset=True),
            owner_id=current_user["id"]
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update property"
            )
        
        # Get updated property
        updated_property = await PropertyService.get_property(property_id)
        
        return updated_property
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update property: {str(e)}"
        )

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: str = Path(..., title="Property ID"),
    current_user: Dict[str, Any] = Depends(require_landlord)
):
    """
    Delete a property.
    
    Only the property owner can delete it.
    """
    # Get property to check ownership
    existing_property = await PropertyService.get_property(property_id)
    
    if not existing_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Check ownership
    if existing_property["owner_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this property"
        )
    
    try:
        # Delete property
        success = await PropertyService.delete_property(property_id, owner_id=current_user["id"])
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete property"
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete property: {str(e)}"
        ) 