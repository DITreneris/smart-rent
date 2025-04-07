"""
Authentication dependencies for FastAPI.
"""
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt import decode_token, verify_token_type

# Configure OAuth2 password bearer for FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Get current user from JWT token.
    
    Args:
        token: JWT token from Authorization header
        
    Returns:
        User data from token
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Decode token
    payload = decode_token(token)
    
    # Verify token type
    if not verify_token_type(payload, "access"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Extract user data from token
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token content",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # In a real implementation, we would fetch the user from the database
    # to ensure they still exist and are active
    # For now, we'll just use the data from the token
    
    # Create user data dictionary
    user_data = {
        "id": user_id,
        "email": payload.get("email"),
        "role": payload.get("role", "user"),
        "permissions": payload.get("permissions", [])
    }
    
    return user_data

async def get_current_active_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Get current active user.
    
    Args:
        current_user: User data from token
        
    Returns:
        User data if active
        
    Raises:
        HTTPException: If user is inactive
    """
    # In a real implementation, we would check if the user is active in the database
    # For now, we'll assume all authenticated users are active
    
    return current_user

def require_roles(required_roles: list[str]):
    """
    Dependency factory for requiring specific roles.
    
    Args:
        required_roles: List of roles allowed to access the endpoint
        
    Returns:
        Dependency function
    """
    async def role_checker(current_user: Dict[str, Any] = Depends(get_current_active_user)) -> Dict[str, Any]:
        user_role = current_user.get("role")
        if user_role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User role '{user_role}' does not have permission to access this resource"
            )
        return current_user
    
    return role_checker

def require_permissions(required_permissions: list[str]):
    """
    Dependency factory for requiring specific permissions.
    
    Args:
        required_permissions: List of permissions required to access the endpoint
        
    Returns:
        Dependency function
    """
    async def permission_checker(current_user: Dict[str, Any] = Depends(get_current_active_user)) -> Dict[str, Any]:
        user_permissions = current_user.get("permissions", [])
        
        # Check if user has all required permissions
        missing_permissions = [p for p in required_permissions if p not in user_permissions]
        
        if missing_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permissions: {', '.join(missing_permissions)}"
            )
        
        return current_user
    
    return permission_checker

# Common role-based dependencies
require_admin = require_roles(["admin"])
require_landlord = require_roles(["admin", "landlord"])
require_tenant = require_roles(["admin", "tenant"])
require_any_user = require_roles(["admin", "landlord", "tenant", "user"]) 