"""
Authentication dependencies for FastAPI.
"""
from typing import Optional, List, Union, Dict, Any
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param

from app.auth.jwt import decode_token, verify_token_permissions
from app.services.auth_service import AuthService

# Define OAuth2 password bearer scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/auth/token",
    auto_error=False
)

# Import DB session dependency and User model
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db # Assuming get_db is here
from app.models.user import User # Import the User model

class RoleChecker:
    """Dependency for checking user roles."""
    
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
        
    def __call__(self, token_data: Dict[str, Any] = Depends(oauth2_scheme)) -> Dict[str, Any]:
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authenticated"
            )
            
        role = token_data.get("role")
        if role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {role} not authorized to access this resource"
            )
            
        return token_data

class PermissionChecker:
    """Dependency for checking user permissions."""
    
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions
        
    def __call__(self, token_data: Dict[str, Any] = Depends(oauth2_scheme)) -> Dict[str, Any]:
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authenticated"
            )
            
        # Admin role has all permissions
        if token_data.get("role") == "admin":
            return token_data
            
        # Check specific permissions
        if not verify_token_permissions(token_data, self.required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to access this resource"
            )
            
        return token_data

async def get_token_from_header(request: Request) -> Optional[str]:
    """Extract token from request header."""
    authorization = request.headers.get("Authorization")
    if not authorization:
        return None
        
    scheme, token = get_authorization_scheme_param(authorization)
    if scheme.lower() != "bearer":
        return None
        
    return token

async def get_token_from_cookie(request: Request) -> Optional[str]:
    """Extract token from cookie."""
    return request.cookies.get("access_token")

async def get_token(
    request: Request,
    token_from_header: Optional[str] = Depends(get_token_from_header)
) -> Optional[str]:
    """Get token from header or cookie."""
    if token_from_header:
        return token_from_header
        
    return await get_token_from_cookie(request)

async def get_current_token_data(token: Optional[str] = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Get current token data from authorization header."""
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    return decode_token(token)

async def get_optional_token_data(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[Dict[str, Any]]:
    """Get token data if available, but don't require it."""
    if token is None:
        return None
        
    try:
        return decode_token(token)
    except HTTPException:
        return None

async def get_current_user(
    db: AsyncSession = Depends(get_db), # Add DB dependency
    token_data: Dict[str, Any] = Depends(get_current_token_data)
) -> User: # Change return type hint to User model
    """Get current user model instance from token data."""
    user_id = token_data.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token contents",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Get user model instance from database
    user = await AuthService.get_user_by_id(db=db, user_id=user_id) # Pass db session
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user # Return the User model instance

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User: # Update type hint and return type
    """Check that the current user is active."""
    if not current_user.is_active: # Access attribute directly
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user

# Role-specific dependencies
get_admin_user = RoleChecker(allowed_roles=["admin"])
get_landlord_user = RoleChecker(allowed_roles=["admin", "landlord"])
get_tenant_user = RoleChecker(allowed_roles=["admin", "tenant"])

# Commonly used permission checkers
can_manage_properties = PermissionChecker(required_permissions=["manage:properties"])
can_view_reports = PermissionChecker(required_permissions=["view:reports"])
can_process_payments = PermissionChecker(required_permissions=["process:payments"]) 