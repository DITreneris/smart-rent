"""
Authentication service for user login and registration.
"""
from typing import Dict, Any, Optional, Tuple, List, Union
from datetime import datetime, timedelta
import hashlib
import os
import secrets
import logging
from passlib.context import CryptContext
from app.auth.jwt import create_access_token, create_refresh_token, decode_refresh_token
from app.models.auth import TokenResponse, LoginRequest, RegisterRequest, UserResponse
from app.models.user import User, UserCreate, UserUpdate
from app.config.settings import settings

# Set up logging
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Service for handling authentication operations."""
    
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
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID to lookup
            
        Returns:
            User data or None if not found
        """
        # In a real implementation, this would query the database
        # For demo purposes, we'll return mock data
        # Replace with actual database query in production
        
        # Mock user database
        users = {
            "1": {
                "id": "1",
                "email": "admin@example.com",
                "password_hash": AuthService.hash_password("admin123"),
                "full_name": "Admin User",
                "role": "admin",
                "is_active": True,
                "permissions": ["manage:all", "view:all"],
                "created_at": datetime(2025, 1, 1)
            },
            "2": {
                "id": "2",
                "email": "landlord@example.com",
                "password_hash": AuthService.hash_password("landlord123"),
                "full_name": "Landlord User",
                "role": "landlord",
                "is_active": True,
                "permissions": ["manage:properties", "view:reports"],
                "created_at": datetime(2025, 1, 2)
            },
            "3": {
                "id": "3",
                "email": "tenant@example.com",
                "password_hash": AuthService.hash_password("tenant123"),
                "full_name": "Tenant User",
                "role": "tenant",
                "is_active": True,
                "permissions": ["view:properties", "request:maintenance"],
                "created_at": datetime(2025, 1, 3)
            }
        }
        
        return users.get(user_id)
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email.
        
        Args:
            email: Email to lookup
            
        Returns:
            User data or None if not found
        """
        # In a real implementation, this would query the database
        # For now, we'll use the mock user database
        users = [
            {
                "id": "1",
                "email": "admin@example.com",
                "password_hash": AuthService.hash_password("admin123"),
                "full_name": "Admin User",
                "role": "admin",
                "is_active": True,
                "permissions": ["manage:all", "view:all"],
                "created_at": datetime(2025, 1, 1)
            },
            {
                "id": "2",
                "email": "landlord@example.com",
                "password_hash": AuthService.hash_password("landlord123"),
                "full_name": "Landlord User",
                "role": "landlord",
                "is_active": True,
                "permissions": ["manage:properties", "view:reports"],
                "created_at": datetime(2025, 1, 2)
            },
            {
                "id": "3",
                "email": "tenant@example.com",
                "password_hash": AuthService.hash_password("tenant123"),
                "full_name": "Tenant User",
                "role": "tenant",
                "is_active": True,
                "permissions": ["view:properties", "request:maintenance"],
                "created_at": datetime(2025, 1, 3)
            }
        ]
        
        for user in users:
            if user["email"] == email:
                return user
                
        return None
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            User data if authentication successful, None otherwise
        """
        # Get user from database
        user = await AuthService.get_user_by_email(email)
        if user is None:
            return None
            
        # Verify password
        if not AuthService.verify_password(password, user["password_hash"]):
            return None
            
        # Check if user is active
        if not user.get("is_active", False):
            return None
            
        return user
    
    @staticmethod
    async def login(login_data: LoginRequest) -> Optional[TokenResponse]:
        """
        Log in user with email and password.
        
        Args:
            login_data: Login credentials
            
        Returns:
            Token response with access and refresh tokens
        """
        # Authenticate user
        user = await AuthService.authenticate_user(login_data.email, login_data.password)
        if user is None:
            return None
            
        # Create tokens
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user["id"])
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserResponse(
                id=user["id"],
                email=user["email"],
                full_name=user.get("full_name", ""),
                role=user.get("role", "user")
            )
        )
    
    @staticmethod
    async def refresh_token(refresh_token: str) -> Optional[TokenResponse]:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            Token response with new access token
        """
        try:
            # Decode refresh token
            user_id = decode_refresh_token(refresh_token)
            
            # Get user from database
            user = await AuthService.get_user_by_id(user_id)
            if user is None:
                return None
                
            # Create new access token
            access_token = create_access_token(user)
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,  # Keep existing refresh token
                token_type="bearer",
                user=UserResponse(
                    id=user["id"],
                    email=user["email"],
                    full_name=user.get("full_name", ""),
                    role=user.get("role", "user")
                )
            )
        except Exception as e:
            logger.error(f"Error refreshing token: {str(e)}")
            return None
    
    @staticmethod
    async def register(user_data: RegisterRequest) -> Optional[UserResponse]:
        """
        Register a new user.
        
        Args:
            user_data: User registration data
            
        Returns:
            Created user response
        """
        # Check if email already exists
        existing_user = await AuthService.get_user_by_email(user_data.email)
        if existing_user is not None:
            return None
            
        # In a real implementation, we would create a new user in the database
        # For now, we'll just return a mock response
        new_user = {
            "id": str(secrets.randbelow(1000000)),
            "email": user_data.email,
            "password_hash": AuthService.hash_password(user_data.password),
            "full_name": user_data.full_name,
            "role": "tenant",  # Default role for new users
            "is_active": True,
            "permissions": ["view:properties"],  # Default permissions
            "created_at": datetime.utcnow()
        }
        
        # In a real implementation, we would save the user to the database
        
        return UserResponse(
            id=new_user["id"],
            email=new_user["email"],
            full_name=new_user["full_name"],
            role=new_user["role"]
        )
    
    @staticmethod
    async def verify_wallet_signature(address: str, message: str, signature: str) -> bool:
        """
        Verify a wallet signature.
        
        Args:
            address: Wallet address
            message: Message that was signed
            signature: Message signature
            
        Returns:
            True if signature is valid, False otherwise
        """
        # In a real implementation, this would validate the signature
        # For demo purposes, we'll return True for specific test values
        
        # Check if this is a test signature
        if address == "0x1234567890123456789012345678901234567890" and \
           message == "Login to SmartRent" and \
           signature.startswith("0x"):
            return True
            
        # Otherwise, perform proper validation
        # This would use web3.py in a real implementation
        # ethereum_message = encode_defunct(text=message)
        # signer = w3.eth.account.recover_message(ethereum_message, signature=signature)
        # return signer.lower() == address.lower()
        
        return False
    
    @staticmethod
    async def login_with_wallet(address: str, message: str, signature: str) -> Optional[TokenResponse]:
        """
        Log in user with wallet signature.
        
        Args:
            address: Wallet address
            message: Message that was signed
            signature: Message signature
            
        Returns:
            Token response with access and refresh tokens if successful
        """
        # Verify signature
        is_valid = await AuthService.verify_wallet_signature(address, message, signature)
        if not is_valid:
            return None
            
        # Get or create user by wallet address
        # In a real implementation, this would query the database
        
        # For demo purposes, we'll create a mock user
        user = {
            "id": "w-" + address[-8:],  # Create ID from last 8 chars of address
            "email": None,  # Wallet users might not have an email initially
            "wallet_address": address,
            "full_name": "Wallet User",
            "role": "tenant",  # Default role for wallet users
            "is_active": True,
            "permissions": ["view:properties"],  # Default permissions
            "created_at": datetime.utcnow()
        }
        
        # Create tokens
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user["id"])
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserResponse(
                id=user["id"],
                email=user.get("email", ""),
                full_name=user.get("full_name", "Wallet User"),
                role=user.get("role", "tenant"),
                wallet_address=address
            )
        )
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using SHA-256.
        
        Args:
            password: Password to hash
            
        Returns:
            Hashed password
        """
        # In a real implementation, we would use a more secure method like bcrypt
        # For demo purposes, we'll use a simple SHA-256 hash
        return hashlib.sha256(password.encode()).hexdigest()
    
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