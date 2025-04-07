from typing import Dict, Generic, List, Optional, Type, TypeVar, Union, Any
import uuid

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base, ModelType


# Type variables for create/update schemas
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository with common CRUD operations for all models
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize repository with model class
        """
        self.model = model
    
    async def get(self, db: AsyncSession, id: uuid.UUID) -> Optional[ModelType]:
        """
        Get a record by ID
        """
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """
        Get multiple records with pagination and optional filters
        """
        query = select(self.model)
        
        # Apply filters if provided
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def count(
        self, 
        db: AsyncSession, 
        *, 
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Count the number of records matching the filters
        """
        query = select(self.model)
        
        # Apply filters if provided
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        
        # Use count() to get the total number of records
        query = select(func.count()).select_from(query.subquery())
        result = await db.execute(query)
        return result.scalar_one()
    
    async def create(
        self, 
        db: AsyncSession, 
        *, 
        obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Create a new record
        """
        # Convert input to dict if it's a Pydantic model
        obj_in_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump()
        
        # Create model instance
        db_obj = self.model(**obj_in_data)
        
        # Add to session and commit
        db.add(db_obj)
        await db.flush()
        
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update a record
        """
        # Convert object to dict
        obj_data = jsonable_encoder(db_obj)
        
        # Get update data
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        
        # Update attributes
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        # Add to session and flush changes
        db.add(db_obj)
        await db.flush()
        
        return db_obj
    
    async def remove(
        self, 
        db: AsyncSession, 
        *, 
        id: uuid.UUID
    ) -> Optional[ModelType]:
        """
        Delete a record by ID
        """
        # Get the object
        obj = await self.get(db, id)
        if obj:
            # Delete and commit
            await db.delete(obj)
            await db.flush()
        
        return obj 