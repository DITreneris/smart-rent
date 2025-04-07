"""
CSRF protection middleware for the SmartRent platform.

Implements the Double Submit Cookie pattern.
"""

import time
from typing import Callable, Optional
from fastapi import Request, Response, HTTPException, status, Depends
from starlette.middleware.base import BaseHTTPMiddleware

from app.routers.auth import token_store, CSRF_COOKIE_NAME


class CSRFMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce CSRF protection using the Double Submit Cookie pattern.
    """
    
    def __init__(self, app):
        super().__init__(app)
        
    async def dispatch(self, request: Request, call_next: Callable):
        """
        Process the request before passing it to the endpoint.
        
        Excludes:
        - GET, HEAD, OPTIONS, TRACE methods as they are considered safe
        - Endpoints marked with route.include_in_schema = False
        - Endpoints with /api/v1/login path
        """
        # Skip CSRF validation for safe methods
        if request.method in ["GET", "HEAD", "OPTIONS", "TRACE"]:
            return await call_next(request)
            
        # Skip CSRF validation for login endpoint
        if request.url.path == "/api/v1/login":
            return await call_next(request)
            
        # Get CSRF cookie from request
        csrf_cookie = request.cookies.get(CSRF_COOKIE_NAME)
        if not csrf_cookie:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF cookie missing"
            )
            
        # Get token from token store
        token_data = token_store.get(csrf_cookie)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid CSRF token"
            )
            
        # Check if token is expired
        if int(time.time()) > token_data["expires"]:
            # Remove expired token
            token_store.pop(csrf_cookie, None)
            
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token expired"
            )
            
        # Get CSRF token from header
        csrf_header = request.headers.get("X-CSRF-Token")
        if not csrf_header:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF header missing"
            )
            
        # Validate CSRF token
        if csrf_header != token_data["value"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token mismatch"
            )
            
        # Continue with the request if validation passed
        return await call_next(request)


def csrf_protect():
    """
    Dependency to protect routes against CSRF attacks.
    Can be used on individual routes that need protection.
    
    Example:
        @router.post("/endpoint", dependencies=[Depends(csrf_protect())])
        async def protected_endpoint():
            ...
    """
    def _csrf_protect(request: Request):
        """Check CSRF token for the request."""
        # Get CSRF cookie from request
        csrf_cookie = request.cookies.get(CSRF_COOKIE_NAME)
        if not csrf_cookie:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF cookie missing"
            )
            
        # Get token from token store
        token_data = token_store.get(csrf_cookie)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid CSRF token"
            )
            
        # Check if token is expired
        if int(time.time()) > token_data["expires"]:
            # Remove expired token
            token_store.pop(csrf_cookie, None)
            
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token expired"
            )
            
        # Get CSRF token from header
        csrf_header = request.headers.get("X-CSRF-Token")
        if not csrf_header:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF header missing"
            )
            
        # Validate CSRF token
        if csrf_header != token_data["value"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token mismatch"
            )
        
        # Return True if validation passed
        return True
        
    return _csrf_protect


async def cleanup_expired_tokens():
    """
    Remove expired tokens from token store.
    Called by background task.
    """
    current_time = time.time()
    expired_tokens = [
        token for token, data in token_store.items()
        if current_time > data["expires"]
    ]
    
    for token in expired_tokens:
        token_store.pop(token, None)
        
    return len(expired_tokens) 