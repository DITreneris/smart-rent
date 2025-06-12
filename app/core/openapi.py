"""
OpenAPI extension configuration for SmartRent API documentation.
"""
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

def custom_openapi(app: FastAPI):
    """
    Create a custom OpenAPI schema for SmartRent API.
    
    This function extends the default OpenAPI schema with:
    - Additional metadata
    - Security schemes
    - Custom documentation templates
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="SmartRent API",
        version="0.5.0",
        description="""
        # SmartRent API Documentation
        
        SmartRent is a blockchain-based property rental platform that connects landlords and tenants.
        
        ## Features
        
        * Property listing and search
        * User authentication and authorization
        * Secure payment processing
        * Smart contract integration
        * Transaction monitoring
        
        ## Authentication
        
        This API uses JWT tokens for authentication. Most endpoints require a valid token.
        
        To authenticate:
        1. Obtain a token via `/api/auth/login` or `/api/auth/register`
        2. Include the token in the Authorization header: `Authorization: Bearer {token}`
        
        ## Rate Limiting
        
        API requests are limited to 100 requests per minute per client.
        """,
        routes=app.routes,
    )
    
    # Add API servers information
    openapi_schema["servers"] = [
        {"url": "https://api.smartrent.com/v1", "description": "Production server"},
        {"url": "https://staging-api.smartrent.com/v1", "description": "Staging server"},
        {"url": "http://localhost:8000", "description": "Local development server"}
    ]
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter JWT token obtained from login/register endpoints"
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [
        {"bearerAuth": []}
    ]
    
    # Add contact information
    openapi_schema["info"]["contact"] = {
        "name": "SmartRent API Support",
        "url": "https://smartrent.com/support",
        "email": "api-support@smartrent.com"
    }
    
    # Add license information
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
    
    # Add terms of service
    openapi_schema["info"]["termsOfService"] = "https://smartrent.com/terms"
    
    # Add tags with descriptions
    openapi_schema["tags"] = [
        {
            "name": "Authentication",
            "description": "Operations related to user authentication and token management"
        },
        {
            "name": "Properties",
            "description": "Operations related to property listings and management"
        },
        {
            "name": "Users",
            "description": "Operations related to user profiles and management"
        },
        {
            "name": "Transactions",
            "description": "Operations related to payment and blockchain transactions"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema 