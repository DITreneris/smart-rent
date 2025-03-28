from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv
import time
import asyncio
from contextlib import asynccontextmanager
from functools import lru_cache

# Import routers
from app.routers import properties, users, contracts, auth

# Load environment variables
load_dotenv()

# Application startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize resources, connections, caches
    print("Server starting up...")
    
    # Initialize app-wide resources
    # These will be available throughout the application's lifetime
    app.state.start_time = time.time()
    
    # Setup any connection pools here
    # Example: app.state.db_pool = await create_db_pool()
    
    yield
    
    # Shutdown: Clean up resources
    print("Server shutting down...")
    
    # Close connection pools here
    # Example: await app.state.db_pool.close()

# Create FastAPI app with lifespan
app = FastAPI(
    title="Smart Rent API",
    description="API for managing rental properties on the blockchain",
    version="1.0.0",
    lifespan=lifespan,
    # Optimize for performance
    openapi_url="/api/v1/openapi.json" if os.getenv("ENVIRONMENT") != "production" else None,
    docs_url="/api/v1/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url="/api/v1/redoc" if os.getenv("ENVIRONMENT") != "production" else None,
)

# Configure CORS
origins = [
    "http://localhost:3000",  # Frontend development
    "http://localhost:8000",  # Backend development
    os.getenv("FRONTEND_URL", "http://localhost:3000")  # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add caching middleware for better performance
@app.middleware("http")
async def add_cache_headers(request, call_next):
    response = await call_next(request)
    
    # Add cache headers for static resources
    if request.url.path.startswith(("/static/", "/api/v1/static/")):
        response.headers["Cache-Control"] = "public, max-age=3600"  # Cache for 1 hour
    
    return response

# Add response time header middleware
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include routers with prefix
api_prefix = "/api/v1"
app.include_router(auth.router, prefix=api_prefix)
app.include_router(users.router, prefix=api_prefix)
app.include_router(properties.router, prefix=api_prefix)
app.include_router(contracts.router, prefix=api_prefix)

# Health check endpoint
@app.get("/health")
@lru_cache(maxsize=1, ttl=5)  # Cache for 5 seconds
async def health_check():
    uptime = time.time() - app.state.start_time
    return {
        "status": "healthy",
        "uptime": uptime
    }

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Default route
@app.get("/")
async def root():
    return {"message": "Welcome to Smart Rent API"}

# Custom exception handler for better error responses
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code},
    )

# Run the application
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    # Use UVicorn with optimized settings
    uvicorn.run(
        "main:app", 
        host=host, 
        port=port, 
        reload=os.getenv("ENVIRONMENT") != "production",
        workers=int(os.getenv("WEB_CONCURRENCY", 1)),  # Use multiple workers for better performance
        loop="uvloop",  # Use uvloop for better async performance
        http="httptools",  # Use httptools for better HTTP parsing performance
        log_level="info"
    ) 