"""
Rate Limiter Middleware

This module provides rate limiting for the FastAPI application.
It implements a sliding window algorithm with Redis backend for
distributed rate limiting.
"""

import time
import hashlib
from typing import Optional, Dict, Callable, List, Union
from fastapi import Request, Response, HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
import redis
from redis.exceptions import RedisError

# Redis connection (use connection pooling in production)
redis_client = None

# Configuration
RATE_LIMIT_ENABLED = True
RATE_LIMIT_REDIS_URL = "redis://localhost:6379/0"  # Move to env variables

# Default rate limits (can be overridden per route)
DEFAULT_RATE_LIMITS = {
    "general": {
        "limit": 100,     # requests
        "window": 60      # seconds
    },
    "auth": {
        "limit": 5,       # requests
        "window": 60      # seconds
    },
    "sensitive": {
        "limit": 10,      # requests
        "window": 60      # seconds
    }
}


class RateLimitExceeded(HTTPException):
    """Rate limit exceeded exception."""

    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(status_code=429, detail=detail)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting."""

    def __init__(self, app, redis_url: str = RATE_LIMIT_REDIS_URL):
        super().__init__(app)
        global redis_client
        # Initialize Redis client if not already initialized
        if redis_client is None:
            redis_client = redis.from_url(redis_url)

    async def dispatch(self, request: Request, call_next):
        """Process the request through the middleware."""
        if not RATE_LIMIT_ENABLED:
            return await call_next(request)

        # Skip rate limiting for non-API endpoints
        if not request.url.path.startswith("/api"):
            return await call_next(request)

        try:
            # Get client identifier
            client_id = self._get_client_id(request)
            
            # Check if rate limited
            rate_limited, remaining, reset_time = await self._check_rate_limit(
                client_id, 
                request.url.path
            )
            
            # If rate limited, return 429 Too Many Requests
            if rate_limited:
                return Response(
                    content={"detail": "Rate limit exceeded, try again later."},
                    status_code=429,
                    media_type="application/json",
                    headers={
                        "X-RateLimit-Limit": str(DEFAULT_RATE_LIMITS["general"]["limit"]),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(reset_time),
                        "Retry-After": str(reset_time - int(time.time()))
                    }
                )
            
            # Proceed with the request
            response = await call_next(request)
            
            # Add rate limit headers to response
            response.headers["X-RateLimit-Limit"] = str(DEFAULT_RATE_LIMITS["general"]["limit"])
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_time)
            
            return response
            
        except RedisError as e:
            # Log the error (in production)
            print(f"Rate limiter error: {str(e)}")
            # Proceed with the request without rate limiting
            return await call_next(request)

    def _get_client_id(self, request: Request) -> str:
        """Get a unique identifier for the client."""
        # Use X-Forwarded-For header if behind a proxy/load balancer
        ip = request.headers.get(
            "X-Forwarded-For", 
            request.client.host if request.client else "unknown"
        ).split(",")[0].strip()
        
        # For authenticated users, include user ID for more granular limits
        # In this example, we assume the user_id is in the request state
        user_id = getattr(request.state, "user_id", None)
        
        if user_id:
            # For authenticated users, combine IP and user ID
            client_key = f"{ip}:{user_id}"
        else:
            # For anonymous users, just use IP
            client_key = ip
            
        # Hash the client key for privacy and to normalize the key length
        return hashlib.md5(client_key.encode()).hexdigest()
        
    async def _check_rate_limit(
        self, 
        client_id: str, 
        path: str
    ) -> tuple[bool, int, int]:
        """
        Check if the request exceeds the rate limit.
        
        Returns a tuple of (is_rate_limited, remaining_requests, reset_time)
        """
        # Determine which rate limit to apply based on the path
        limit_key = "general"
        if path.startswith("/api/auth"):
            limit_key = "auth"
        elif path.startswith("/api/admin") or path.startswith("/api/payments"):
            limit_key = "sensitive"
            
        # Get the rate limit config
        limit_config = DEFAULT_RATE_LIMITS[limit_key]
        limit = limit_config["limit"]
        window = limit_config["window"]
        
        # Create a Redis key for this client and endpoint type
        redis_key = f"ratelimit:{limit_key}:{client_id}"
        
        # Get current timestamp
        now = int(time.time())
        
        # Calculate the window start time
        window_start = now - window
        
        try:
            # Use Redis pipeline for atomic operations
            pipe = redis_client.pipeline()
            
            # Remove timestamps older than the current window
            pipe.zremrangebyscore(redis_key, 0, window_start)
            
            # Count requests in the current window
            pipe.zcard(redis_key)
            
            # Add the current request timestamp to the sorted set
            pipe.zadd(redis_key, {str(now): now})
            
            # Set the key to expire after the window to clean up Redis
            pipe.expire(redis_key, window * 2)
            
            # Execute the pipeline
            _, current_count, _, _ = pipe.execute()
            
            # Calculate remaining requests
            remaining = max(0, limit - current_count - 1)  # -1 for the current request
            
            # Calculate when the rate limit will reset
            oldest_timestamp = redis_client.zrange(redis_key, 0, 0, withscores=True)
            if oldest_timestamp:
                reset_time = int(oldest_timestamp[0][1]) + window
            else:
                reset_time = now + window
                
            # Check if rate limited
            is_rate_limited = current_count >= limit
            
            return is_rate_limited, remaining, reset_time
            
        except RedisError:
            # If Redis fails, don't rate limit
            return False, limit, now + window


def rate_limit(
    limit: int = None, 
    window: int = None,
    key_func: Callable[[Request], str] = None
):
    """
    Dependency function for rate limiting specific endpoints.
    Can override the default limits per route.
    
    Args:
        limit: Maximum number of requests in the window
        window: Time window in seconds
        key_func: Optional function to generate the rate limit key
    """
    
    async def _rate_limit(request: Request):
        if not RATE_LIMIT_ENABLED:
            return True
            
        try:
            # Determine client ID
            if key_func:
                client_id = key_func(request)
            else:
                # Use middleware's client ID function
                client_id = RateLimitMiddleware._get_client_id(None, request)
                
            # Use custom limits if provided, else use general limits
            actual_limit = limit or DEFAULT_RATE_LIMITS["general"]["limit"]
            actual_window = window or DEFAULT_RATE_LIMITS["general"]["window"]
            
            # Create a custom Redis key for this specific rate limit
            path_hash = hashlib.md5(request.url.path.encode()).hexdigest()[:8]
            redis_key = f"ratelimit:custom:{path_hash}:{client_id}"
            
            # Implement rate limiting logic similar to middleware
            now = int(time.time())
            window_start = now - actual_window
            
            pipe = redis_client.pipeline()
            pipe.zremrangebyscore(redis_key, 0, window_start)
            pipe.zcard(redis_key)
            pipe.zadd(redis_key, {str(now): now})
            pipe.expire(redis_key, actual_window * 2)
            _, current_count, _, _ = pipe.execute()
            
            if current_count >= actual_limit:
                raise RateLimitExceeded(
                    f"Rate limit of {actual_limit} requests per {actual_window} seconds exceeded"
                )
                
            return True
            
        except RedisError as e:
            # Log the error (in production)
            print(f"Rate limiter dependency error: {str(e)}")
            # Allow the request in case of errors
            return True
            
    return _rate_limit


# Utility function to enable/disable rate limiting
def configure_rate_limiter(enabled: bool = True, redis_url: str = None):
    """Configure the rate limiter."""
    global RATE_LIMIT_ENABLED, RATE_LIMIT_REDIS_URL, redis_client
    
    RATE_LIMIT_ENABLED = enabled
    
    if redis_url:
        RATE_LIMIT_REDIS_URL = redis_url
        # Reinitialize Redis client with new URL
        redis_client = redis.from_url(redis_url) 