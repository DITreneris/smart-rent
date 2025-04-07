"""
Authentication service for user login and registration.
"""
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
import hashlib
import os
from passlib.context import CryptContext
from app.auth.jwt import create_access_token, create_refresh_token
from app.config.settings import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Service for user authentication."""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password
            
        Returns:
            True if password matches hash, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash password.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def generate_wallet_connection_nonce() -> str:
        """
        Generate a secure nonce for wallet connection.
        
        Returns:
            Secure random nonce string
        """
        # Generate a random 16-byte nonce
        nonce = os.urandom(16).hex()
        return nonce
    
    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with username and password.
        
        Args:
            username: Username or email
            password: Plain text password
            
        Returns:
            User data if authenticated, None otherwise
        """
        # In a real implementation, we would fetch the user from the database
        # For now, we'll use a mock user for demonstration
        
        # Mock user - in production, this would be fetched from the database
        if username == "demo@smartrent.com" and password == "password123":
            return {
                "id": "user-123",
                "email": "demo@smartrent.com",
                "role": "landlord",
                "name": "Demo User",
                "wallet_address": "0x1234567890abcdef1234567890abcdef12345678"
            }
        
        return None
    
    @classmethod
    async def authenticate_wallet(cls, wallet_address: str, signature: str, nonce: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with wallet signature.
        
        Args:
            wallet_address: Ethereum wallet address
            signature: Signature of the nonce
            nonce: Nonce that was signed
            
        Returns:
            User data if authenticated, None otherwise
        """
        # In a real implementation, we would:
        # 1. Verify the signature matches the wallet address and nonce
        # 2. Check if the nonce is valid and not expired
        # 3. Fetch the user associated with this wallet address
        
        # For now, we'll use a mock user for demonstration
        if wallet_address.lower() == "0x1234567890abcdef1234567890abcdef12345678".lower():
            return {
                "id": "user-456",
                "wallet_address": wallet_address,
                "role": "tenant",
                "name": "Wallet User"
            }
        
        return None
    
    @classmethod
    async def generate_tokens(cls, user_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate access and refresh tokens for a user.
        
        Args:
            user_data: User data to encode in tokens
            
        Returns:
            Dictionary with access and refresh tokens
        """
        # Create token data with minimal required fields
        token_data = {
            "sub": user_data["id"],
            "role": user_data.get("role", "user")
        }
        
        # Add optional fields if available
        if "email" in user_data:
            token_data["email"] = user_data["email"]
        
        if "wallet_address" in user_data:
            token_data["wallet_address"] = user_data["wallet_address"]
        
        # Generate tokens
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    @classmethod
    async def register_user(cls, user_data: Dict[str, Any], password: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        Register a new user.
        
        Args:
            user_data: User registration data
            password: Plain text password
            
        Returns:
            Tuple of (user_data, tokens)
        """
        # In a real implementation, we would:
        # 1. Validate the user data
        # 2. Hash the password
        # 3. Store the user in the database
        # 4. Generate tokens
        
        # For demonstration, we'll just return mock data
        
        # Hash password
        hashed_password = cls.get_password_hash(password)
        
        # Create user data
        new_user = {
            "id": f"user-{os.urandom(4).hex()}",
            "email": user_data["email"],
            "name": user_data.get("name", ""),
            "role": "user",  # Default role
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True
        }
        
        # Generate tokens
        tokens = await cls.generate_tokens(new_user)
        
        return new_user, tokens 