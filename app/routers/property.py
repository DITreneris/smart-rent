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
    PropertyStatus,
    PropertyCreate,
    PropertyUpdate,
    PropertySearchParams
)
from app.services.property_service import PropertyService
from app.auth.dependencies import get_current_active_user, get_landlord_user, can_manage_properties
from app.models.auth import ErrorResponse

# Create router
router = APIRouter(
    prefix="/api/properties",
    tags=["Properties"],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)

@router.post("", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_data: PropertyCreate,
    current_user: Dict[str, Any] = Depends(get_landlord_user)
):
    """
    Create a new property listing.
    
    Only landlords and admins can create properties.
    """
    # Create the property
    property_db = await PropertyService.create_property(property_data, current_user["id"])
    
    return property_db

@router.get("", response_model=List[PropertyResponse])
async def search_properties(
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_bedrooms: Optional[int] = None,
    max_bedrooms: Optional[int] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    country: Optional[str] = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_active_user)
):
    """
    Search for properties with filters.
    """
    # Create search parameters
    search_params = PropertySearchParams(
        property_type=property_type,
        min_price=min_price,
        max_price=max_price,
        min_bedrooms=min_bedrooms,
        max_bedrooms=max_bedrooms,
        city=city,
        state=state,
        country=country
    )
    
    # Search properties
    properties = await PropertyService.search_properties(
        search_params=search_params,
        limit=limit,
        offset=offset
    )
    
    return properties

@router.get("/my", response_model=List[PropertyResponse])
async def get_my_properties(
    current_user: Dict[str, Any] = Depends(get_landlord_user)
):
    """
    Get properties owned by the current user.
    
    Only landlords and admins can access this endpoint.
    """
    # Get properties by owner
    properties = await PropertyService.get_properties_by_owner(current_user["id"])
    
    return properties

@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: str = Path(..., description="The ID of the property"),
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Get a property by ID.
    """
    # Get the property
    property_db = await PropertyService.get_property(property_id)
    
    # Check if property exists
    if not property_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    return property_db

@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_data: PropertyUpdate,
    property_id: str = Path(..., description="The ID of the property"),
    current_user: Dict[str, Any] = Depends(get_landlord_user)
):
    """
    Update a property.
    
    Only the owner or admin can update a property.
    """
    # Update the property
    updated_property = await PropertyService.update_property(
        property_id=property_id,
        property_data=property_data,
        owner_id=current_user["id"]
    )
    
    # Check if property exists and user is the owner
    if not updated_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found or you don't have permission to update it"
        )
    
    return updated_property

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: str = Path(..., description="The ID of the property"),
    current_user: Dict[str, Any] = Depends(get_landlord_user)
):
    """
    Delete a property.
    
    Only the owner or admin can delete a property.
    """
    # Delete the property
    success = await PropertyService.delete_property(
        property_id=property_id,
        owner_id=current_user["id"]
    )
    
    # Check if property exists and user is the owner
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found or you don't have permission to delete it"
        )
    
    return None 