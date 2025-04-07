from datetime import datetime
import uuid
from typing import Any, Dict, TypeVar

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    Base class for all database models
    
    Includes common attributes and methods for all models:
    - id: UUID primary key
    - created_at: Timestamp when the record was created
    - updated_at: Timestamp when the record was last updated
    - __tablename__: Automatically generated from the class name
    """
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Fields for type annotation
    __name__: str
    
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table name from class name
        ConvertCamelCaseToSnakeCase
        """
        # Convert camel case to snake case
        name = cls.__name__
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
    
    def dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Type variable for models that extend Base
ModelType = TypeVar("ModelType", bound=Base) 