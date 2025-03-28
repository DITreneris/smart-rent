from fastapi import APIRouter, Depends, HTTPException, Query, Path, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models
from ..database import get_db
from ..schemas import properties as property_schemas
from .auth import get_current_active_user
from functools import lru_cache
import asyncio
import time

router = APIRouter(
    prefix="/properties",
    tags=["properties"],
    responses={404: {"description": "Not found"}},
)

# Cache of recently accessed properties to reduce blockchain queries
property_cache = {}
CACHE_TTL = 300  # 5 minutes

# Cache cleanup background task
async def cleanup_cache():
    """Remove expired cache entries"""
    current_time = time.time()
    expired_keys = [
        key for key, (data, timestamp) in property_cache.items() 
        if current_time - timestamp > CACHE_TTL
    ]
    for key in expired_keys:
        del property_cache[key]

@router.get("/", response_model=List[property_schemas.PropertyResponse])
async def read_properties(
    background_tasks: BackgroundTasks,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    location: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    available_only: bool = False,
    current_user = Depends(get_current_active_user)
):
    """
    Get all properties with optional filtering.
    - **skip**: Number of properties to skip
    - **limit**: Maximum number of properties to return
    - **location**: Filter properties by location
    - **min_price**: Filter properties with price >= min_price
    - **max_price**: Filter properties with price <= max_price
    - **available_only**: If true, only return available properties
    """
    # Schedule cache cleanup in the background
    background_tasks.add_task(cleanup_cache)
    
    # Generate cache key based on filter parameters
    cache_key = f"properties:{skip}:{limit}:{location}:{min_price}:{max_price}:{available_only}"
    
    # Check if we have a cached result
    if cache_key in property_cache:
        data, timestamp = property_cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            return data
    
    # Get properties from blockchain
    try:
        properties = await get_all_properties()
        
        # Apply filters
        if location:
            properties = [p for p in properties if location.lower() in p.location.lower()]
        if min_price is not None:
            properties = [p for p in properties if p.price >= min_price]
        if max_price is not None:
            properties = [p for p in properties if p.price <= max_price]
        if available_only:
            properties = [p for p in properties if p.available]
            
        # Apply pagination
        results = properties[skip:skip + limit]
        
        # Cache the results
        property_cache[cache_key] = (results, time.time())
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch properties: {str(e)}")

@router.get("/{property_id}", response_model=property_schemas.PropertyResponse)
async def read_property(
    property_id: int = Path(..., gt=0),
    current_user = Depends(get_current_active_user)
):
    """
    Get a specific property by ID.
    - **property_id**: The ID of the property to retrieve
    """
    # Check cache first
    cache_key = f"property:{property_id}"
    if cache_key in property_cache:
        data, timestamp = property_cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            return data
    
    # Get property from blockchain
    try:
        property_item = await get_property_by_id(property_id)
        if not property_item:
            raise HTTPException(status_code=404, detail="Property not found")
        
        # Cache the result
        property_cache[cache_key] = (property_item, time.time())
        
        return property_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch property: {str(e)}")

@router.post("/", response_model=property_schemas.PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_new_property(
    property_data: property_schemas.PropertyCreate,
    current_user = Depends(get_current_active_user)
):
    """
    Create a new property.
    """
    try:
        # Validate owner is the current user
        if property_data.owner_id != current_user.id:
            raise HTTPException(
                status_code=403, 
                detail="You can only create properties for yourself"
            )
        
        # Create property in blockchain
        new_property = await create_property(property_data)
        
        # Invalidate cache for property list
        keys_to_remove = [k for k in property_cache if k.startswith("properties:")]
        for k in keys_to_remove:
            del property_cache[k]
        
        return new_property
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create property: {str(e)}")

@router.put("/{property_id}", response_model=property_schemas.PropertyResponse)
async def update_existing_property(
    property_data: property_schemas.PropertyUpdate,
    property_id: int = Path(..., gt=0),
    current_user = Depends(get_current_active_user)
):
    """
    Update an existing property.
    - **property_id**: The ID of the property to update
    """
    try:
        # Get current property
        property_item = await get_property_by_id(property_id)
        if not property_item:
            raise HTTPException(status_code=404, detail="Property not found")
        
        # Check if user is owner
        if property_item.owner_id != current_user.id:
            raise HTTPException(
                status_code=403, 
                detail="You can only update your own properties"
            )
        
        # Update property in blockchain
        updated_property = await update_property(property_id, property_data)
        
        # Invalidate cache
        keys_to_remove = [k for k in property_cache if k.startswith("properties:") or k == f"property:{property_id}"]
        for k in keys_to_remove:
            del property_cache[k]
        
        return updated_property
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update property: {str(e)}")

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_property(
    property_id: int = Path(..., gt=0),
    current_user = Depends(get_current_active_user)
):
    """
    Delete a property.
    - **property_id**: The ID of the property to delete
    """
    try:
        # Get current property
        property_item = await get_property_by_id(property_id)
        if not property_item:
            raise HTTPException(status_code=404, detail="Property not found")
        
        # Check if user is owner
        if property_item.owner_id != current_user.id:
            raise HTTPException(
                status_code=403, 
                detail="You can only delete your own properties"
            )
        
        # Delete property from blockchain
        await delete_property(property_id)
        
        # Invalidate cache
        keys_to_remove = [k for k in property_cache if k.startswith("properties:") or k == f"property:{property_id}"]
        for k in keys_to_remove:
            del property_cache[k]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete property: {str(e)}") 