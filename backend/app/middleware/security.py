from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
from typing import Callable

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"
        
        return response

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log request details
        print(f"{request.method} {request.url.path} - Status: {response.status_code} - Duration: {process_time:.4f}s")
        
        return response

class RateLimitingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_limit: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.requests = {}  # IP -> list of timestamps
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client IP
        client_ip = request.client.host
        
        # Get current time
        current_time = time.time()
        
        # Initialize or update timestamps for this IP
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Remove timestamps older than the window
        self.requests[client_ip] = [
            ts for ts in self.requests[client_ip] if ts > current_time - self.window_seconds
        ]
        
        # Check if we've exceeded the request limit
        if len(self.requests[client_ip]) >= self.requests_limit:
            return Response(status_code=429, text="Too many requests")
        
        # Process the request
        response = await call_next(request)
        
        # Add current timestamp to the list
        self.requests[client_ip].append(current_time)
        
        return response 