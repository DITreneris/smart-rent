"""
Main FastAPI application.
"""

import logging
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.redoc import get_redoc_html
import uvicorn
from typing import List

from app.routers import auth_router, property_router, proposal_router, metadata_router
from app.core.config import settings
from app.core.openapi import custom_openapi

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI application
app = FastAPI(
    title="SmartRent API",
    description="API for blockchain-based property rental platform",
    version="0.5.0",
    openapi_url="/api/openapi.json",
    docs_url=None,
    redoc_url=None
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add session middleware
app.add_middleware(
    SessionMiddleware, 
    secret_key=settings.SECRET_KEY
)

# Include routers
app.include_router(auth_router)
app.include_router(property_router)
app.include_router(
    proposal_router, 
    prefix="/api/v1/proposals", 
    tags=["proposals"]
)
app.include_router(
    metadata_router,
    prefix="/api/v1/metadata",
    tags=["metadata"]
)

# Custom OpenAPI schema
app.openapi = lambda: custom_openapi(app)

@app.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI with branded theme"""
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="SmartRent API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
        swagger_favicon_url="/static/favicon.ico",
        oauth2_redirect_url="/api/docs/oauth2-redirect",
        init_oauth={
            "clientId": "",
            "clientSecret": "",
            "realm": "smartrent",
            "appName": "SmartRent API",
            "scopeSeparator": " ",
            "scopes": "read:properties write:properties",
            "additionalQueryStringParams": {}
        }
    )

@app.get("/api/redoc", include_in_schema=False)
async def redoc_html():
    """Custom ReDoc UI"""
    return get_redoc_html(
        openapi_url="/api/openapi.json",
        title="SmartRent API Documentation",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.0.0/bundles/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.ico"
    )

@app.get("/")
async def root():
    """Root endpoint for SmartRent API"""
    return {
        "message": "Welcome to SmartRent API",
        "version": "0.5.0",
        "documentation": "/api/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions"""
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."}
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    ) 