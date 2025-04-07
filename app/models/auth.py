"""
Authentication models for API requests and responses.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
import re
from datetime import datetime

class TokenResponse(BaseModel):
    """Token response model."""
    access_token: str
    refresh_token: str
    token_type: str
    user: 'UserResponse'
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "1",
                    "email": "user@example.com",
                    "full_name": "John Doe",
                    "role": "tenant"
                }
            }
        }

class LoginRequest(BaseModel):
    """Login request model."""
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        }

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
    
    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }

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
    message: str
    
    class Config:
        schema_extra = {
            "example": {
                "nonce": "a1b2c3d4e5f6",
                "message": "Sign this message to authenticate with SmartRent: a1b2c3d4e5f6"
            }
        }

class UserResponse(BaseModel):
    """User response model."""
    id: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str
    wallet_address: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "email": "user@example.com",
                "full_name": "John Doe",
                "role": "tenant"
            }
        }

class RegisterRequest(BaseModel):
    """Registration request model."""
    email: EmailStr
    password: str
    password_confirm: str
    full_name: str
    
    @validator('password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "email": "newuser@example.com",
                "password": "strongpassword123",
                "password_confirm": "strongpassword123",
                "full_name": "New User"
            }
        }

class WalletAuthRequest(BaseModel):
    """Wallet authentication request model."""
    address: str
    message: str
    signature: str
    
    class Config:
        schema_extra = {
            "example": {
                "address": "0x1234567890123456789012345678901234567890",
                "message": "Login to SmartRent",
                "signature": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1b"
            }
        }

class WalletNonceRequest(BaseModel):
    """Wallet nonce request model."""
    address: str
    
    class Config:
        schema_extra = {
            "example": {
                "address": "0x1234567890123456789012345678901234567890"
            }
        }

class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "Invalid credentials"
            }
        } 