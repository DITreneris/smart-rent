"""
Authentication models for API requests and responses.
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
import re

class TokenResponse(BaseModel):
    """Token response model."""
    access_token: str
    refresh_token: str
    token_type: str

class LoginRequest(BaseModel):
    """Login request model."""
    username: str
    password: str

class WalletLoginRequest(BaseModel):
    """Wallet-based login request model."""
    wallet_address: str
    signature: str
    nonce: str
    
    @validator('wallet_address')
    def validate_wallet_address(cls, v):
        """Validate wallet address format."""
        if not re.match(r'^0x[a-fA-F0-9]{40}$', v):
            raise ValueError('Invalid Ethereum wallet address format')
        return v.lower()

class RefreshTokenRequest(BaseModel):
    """Refresh token request model."""
    refresh_token: str

class UserRegistrationRequest(BaseModel):
    """User registration request model."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: Optional[str] = None
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength."""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        return v

class WalletRegistrationRequest(BaseModel):
    """Wallet-based registration request model."""
    wallet_address: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    
    @validator('wallet_address')
    def validate_wallet_address(cls, v):
        """Validate wallet address format."""
        if not re.match(r'^0x[a-fA-F0-9]{40}$', v):
            raise ValueError('Invalid Ethereum wallet address format')
        return v.lower()

class WalletNonceResponse(BaseModel):
    """Wallet nonce response model."""
    nonce: str
    expires_at: str

class UserResponse(BaseModel):
    """User response model."""
    id: str
    email: Optional[str] = None
    name: Optional[str] = None
    role: str
    wallet_address: Optional[str] = None
    is_active: bool = True 