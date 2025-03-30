from fastapi import FastAPI

from app.api.endpoints import auth, properties
from app.core.config import settings
from app.middleware.security import setup_security_middleware

app = FastAPI(title="SmartRent API")

# Setup security middleware
app = setup_security_middleware(app)

# Include routers
app.include_router(
    auth.router, 
    prefix=f"{settings.API_V1_STR}/auth", 
    tags=["authentication"]
)
app.include_router(
    properties.router, 
    prefix=f"{settings.API_V1_STR}/properties", 
    tags=["properties"]
)

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"} 