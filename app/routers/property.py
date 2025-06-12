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
        401: {"model": ErrorResponse, "description": "Unauthorized - Invalid or expired token"},
        403: {"model": ErrorResponse, "description": "Forbidden - Insufficient permissions"},
        404: {"model": ErrorResponse, "description": "Not Found - Resource does not exist"},
        500: {"model": ErrorResponse, "description": "Internal Server Error - Server-side error"}
    }
)

@router.post(
    "", 
    response_model=PropertyResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new property listing",
    response_description="The created property with its ID and timestamp"
)
async def create_property(
    property_data: PropertyCreate,
    current_user: Dict[str, Any] = Depends(get_landlord_user)
):
    """
    Create a new property listing with the provided details.
    
    ## Authorization
    - Requires authentication with landlord or admin role
    
    ## Request Body
    - **title**: Property title (required)
    - **description**: Detailed description
    - **property_type**: Type of property (e.g., apartment, house)
    - **price**: Monthly rental price (required)
    - **address**: Property address details
    - **features**: List of property features
    - **is_available**: Whether the property is available for rent
    
    ## Returns
    The created property with status code 201
    
    ## Example
    ```json
    {
        "title": "Modern Downtown Apartment",
        "description": "Beautiful apartment in city center",
        "property_type": "apartment",
        "price": 1200,
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001",
            "country": "USA"
        },
        "features": ["parking", "elevator", "pet-friendly"],
        "is_available": true
    }
    ```
    """
    # Create the property
    property_db = await PropertyService.create_property(property_data, current_user["id"])
    
    return property_db

@router.get(
    "", 
    response_model=List[PropertyResponse],
    summary="Search properties with filters",
    response_description="List of properties matching the search criteria"
)
async def search_properties(
    property_type: Optional[str] = Query(None, description="Filter by property type (e.g., apartment, house)"),
    min_price: Optional[float] = Query(None, description="Minimum monthly price"),
    max_price: Optional[float] = Query(None, description="Maximum monthly price"),
    min_bedrooms: Optional[int] = Query(None, description="Minimum number of bedrooms"),
    max_bedrooms: Optional[int] = Query(None, description="Maximum number of bedrooms"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/province"),
    country: Optional[str] = Query(None, description="Filter by country"),
    limit: int = Query(default=10, ge=1, le=100, description="Number of results to return (max 100)"),
    offset: int = Query(default=0, ge=0, description="Number of results to skip (pagination)"),
    current_user: Optional[Dict[str, Any]] = Depends(get_current_active_user)
):
    """
    Search for properties with various filters and pagination.
    
    ## Authorization
    - Requires authentication
    
    ## Parameters
    All filter parameters are optional and can be combined
    
    ## Returns
    List of properties matching the criteria
    
    ## Example
    ```
    GET /api/properties?property_type=apartment&min_price=800&max_price=1500&city=New%20York&limit=20&offset=0
    ```
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

@router.get(
    "/my", 
    response_model=List[PropertyResponse],
    summary="Get properties owned by current user",
    response_description="List of properties owned by the authenticated user"
)
async def get_my_properties(
    current_user: Dict[str, Any] = Depends(get_landlord_user)
):
    """
    Get properties owned by the authenticated user.
    
    ## Authorization
    - Requires authentication with landlord or admin role
    
    ## Returns
    List of properties owned by the current user
    
    ## Example
    ```
    GET /api/properties/my
    ```
    """
    # Get properties by owner
    properties = await PropertyService.get_properties_by_owner(current_user["id"])
    
    return properties

@router.get(
    "/{property_id}", 
    response_model=PropertyResponse,
    summary="Get property by ID",
    response_description="Detailed property information"
)
async def get_property(
    property_id: str = Path(..., description="The ID of the property to retrieve"),
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Get detailed information for a specific property.
    
    ## Authorization
    - Requires authentication
    
    ## Path Parameters
    - **property_id**: Unique identifier of the property
    
    ## Returns
    The property details if found
    
    ## Raises
    - 404: Property not found
    
    ## Example
    ```
    GET /api/properties/5f8d0e352b15f22e2081b2a8
    ```
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

@router.put(
    "/{property_id}", 
    response_model=PropertyResponse,
    summary="Update property details",
    response_description="Updated property information"
)
async def update_property(
    property_data: PropertyUpdate,
    property_id: str = Path(..., description="The ID of the property to update"),
    current_user: Dict[str, Any] = Depends(get_landlord_user)
):
    """
    Update an existing property listing.
    
    ## Authorization
    - Requires authentication with landlord or admin role
    - Only the owner or an admin can update the property
    
    ## Path Parameters
    - **property_id**: Unique identifier of the property
    
    ## Request Body
    Fields to update (all are optional):
    - **title**: Property title
    - **description**: Detailed description
    - **property_type**: Type of property
    - **price**: Monthly rental price
    - **address**: Property address details
    - **features**: List of property features
    - **is_available**: Whether the property is available for rent
    
    ## Returns
    The updated property details
    
    ## Raises
    - 404: Property not found or user doesn't have permission
    
    ## Example
    ```json
    {
        "price": 1350,
        "is_available": false,
        "features": ["parking", "elevator", "pet-friendly", "balcony"]
    }
    ```
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

@router.delete(
    "/{property_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a property",
    response_description="No content is returned upon successful deletion"
)
async def delete_property(
    property_id: str = Path(..., description="The ID of the property to delete"),
    current_user: Dict[str, Any] = Depends(get_landlord_user)
):
    """
    Delete a property listing.
    
    ## Authorization
    - Requires authentication with landlord or admin role
    - Only the owner or an admin can delete the property
    
    ## Path Parameters
    - **property_id**: Unique identifier of the property
    
    ## Returns
    - 204: No content on successful deletion
    
    ## Raises
    - 404: Property not found or user doesn't have permission
    
    ## Example
    ```
    DELETE /api/properties/5f8d0e352b15f22e2081b2a8
    ```
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