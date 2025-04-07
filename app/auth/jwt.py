"""
JWT authentication utilities.
"""
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, Union
from fastapi import HTTPException, status
from pydantic import BaseModel
from app.config.settings import settings

# Define models for token payloads
class TokenPayload(BaseModel):
    sub: str
    exp: datetime
    iat: datetime
    role: str
    permissions: Optional[list] = None

class TokenData(BaseModel):
    user_id: str
    role: str
    permissions: Optional[list] = None

def create_access_token(user_data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token.
    
    Args:
        user_data: User data to encode in token (must include id and role)
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    # Set token expiry time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create payload
    to_encode = {
        "sub": str(user_data["id"]),
        "exp": expire,
        "iat": datetime.utcnow(),
        "role": user_data.get("role", "user")
    }
    
    # Add custom claims if available
    if "permissions" in user_data:
        to_encode["permissions"] = user_data["permissions"]
    
    # Create token
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(user_id: str) -> str:
    """
    Create a refresh token with longer expiration.
    
    Args:
        user_id: User ID to encode in token
        
    Returns:
        Encoded JWT refresh token string
    """
    # Set refresh token expiry (typically longer than access token)
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Create minimal payload (just user ID and expiration)
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.utcnow(),
        "token_type": "refresh"
    }
    
    # Create token with different key
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.REFRESH_TOKEN_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_token(token: str, verify_exp: bool = True) -> Dict[str, Any]:
    """
    Decode and validate JWT token.
    
    Args:
        token: JWT token to decode
        verify_exp: Whether to verify token expiration
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": verify_exp}
        )
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

def decode_refresh_token(token: str) -> str:
    """
    Decode and validate refresh token.
    
    Args:
        token: Refresh token to decode
        
    Returns:
        User ID from the token
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token, 
            settings.REFRESH_TOKEN_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Verify it's a refresh token
        if payload.get("token_type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        return user_id
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Refresh token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )

def verify_token_permissions(token_data: Dict[str, Any], required_permissions: list) -> bool:
    """
    Verify if token has required permissions.
    
    Args:
        token_data: Decoded token data
        required_permissions: List of required permissions
        
    Returns:
        True if token has all required permissions, False otherwise
    """
    if "permissions" not in token_data:
        return False
        
    user_permissions = token_data["permissions"]
    return all(perm in user_permissions for perm in required_permissions) 