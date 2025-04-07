"""
Router package for API endpoints.
"""
from app.routers.auth import router as auth_router
from app.routers.property import router as property_router

__all__ = [
    "auth_router",
    "property_router"
] 