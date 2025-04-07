"""
JWT authentication utilities.
"""
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from fastapi import HTTPException, status
from app.config.settings import settings

def create_access_token(user_data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token.
    
    Args:
        user_data: User data to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token as string
    """
    # Create a copy of the data to avoid modifying the original
    to_encode = user_data.copy()
    
    # Set token expiry time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add token claims
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "token_type": "access"
    })
    
    # Create token
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def create_refresh_token(user_data: Dict[str, Any]) -> str:
    """
    Create a new JWT refresh token.
    
    Args:
        user_data: User data to encode in the token
        
    Returns:
        Encoded JWT token as string
    """
    # Create a copy of the data to avoid modifying the original
    to_encode = user_data.copy()
    
    # Set token expiry time - refresh tokens last longer
    expire = datetime.utcnow() + timedelta(days=7)
    
    # Add token claims
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "token_type": "refresh"
    })
    
    # Create token
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate JWT token.
    
    Args:
        token: JWT token to decode
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
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

def verify_token_type(payload: Dict[str, Any], expected_type: str) -> bool:
    """
    Verify token is of the expected type.
    
    Args:
        payload: Decoded token payload
        expected_type: Expected token type ('access' or 'refresh')
        
    Returns:
        True if token is of expected type, False otherwise
    """
    token_type = payload.get("token_type")
    if token_type != expected_type:
        return False
    return True 