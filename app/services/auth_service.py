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
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
        return os.urandom(16).hex()
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
        """
        Get user by ID from database (Async).
        
        Args:
            db: The AsyncSession instance.
            user_id: User ID to lookup.
            
        Returns:
            SQLAlchemy User model instance or None if not found.
        """
        logger.debug(f"Attempting to fetch user by ID: {user_id}")
        try:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalars().first()
            if user:
                 logger.debug(f"User found: {user.email}")
            else:
                 logger.debug(f"User with ID {user_id} not found.")
            return user
        except Exception as e:
            logger.error(f"Database error fetching user by ID {user_id}: {e}", exc_info=True)
            # Depending on policy, might re-raise or return None
            # Returning None is often safer for auth checks
            return None
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """
        Get user by email from database (Async).
        
        Args:
            db: The AsyncSession instance.
            email: Email to lookup.
            
        Returns:
            SQLAlchemy User model instance or None if not found.
        """
        logger.debug(f"Attempting to fetch user by email: {email}")
        try:
            stmt = select(User).where(User.email == email)
            result = await db.execute(stmt)
            user = result.scalars().first()
            if user:
                 logger.debug(f"User found: {user.email}")
            else:
                 logger.debug(f"User with email {email} not found.")
            return user
        except Exception as e:
            logger.error(f"Database error fetching user by email {email}: {e}", exc_info=True)
            return None # Safer for auth checks
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password (Async).
        
        Args:
            db: The AsyncSession instance.
            email: User email.
            password: User password.
            
        Returns:
            User model instance if authentication successful, None otherwise.
        """
        user = await AuthService.get_user_by_email(db, email)
        if user is None:
            logger.warning(f"Authentication failed: User not found for email {email}")
            return None
            
        # Verify password (Sync operation)
        if not AuthService.verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed: Invalid password for email {email}")
            return None
            
        # Check if user is active (Sync operation)
        if not user.is_active:
            logger.warning(f"Authentication failed: User {email} is inactive.")
            return None
            
        logger.info(f"User {email} authenticated successfully.")
        return user
    
    @staticmethod
    async def login(db: AsyncSession, login_data: LoginRequest) -> Optional[TokenResponse]:
        """
        Log in user with email and password (Async).
        """
        # Authenticate user (Async)
        user = await AuthService.authenticate_user(db, login_data.email, login_data.password)
        if user is None:
            return None # Auth failed
            
        # Create tokens (Sync)
        # Ensure create_access_token expects User model or adapt it
        access_token = create_access_token(user) 
        refresh_token = create_refresh_token(user.id)
        
        # Ensure UserResponse expects model or adapt it
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=user_response
        )
    
    @staticmethod
    async def refresh_token(db: AsyncSession, refresh_token: str) -> Optional[TokenResponse]:
        """
        Refresh access token using refresh token (Async).
        """
        try:
            # Decode refresh token (Sync)
            user_id = decode_refresh_token(refresh_token)
            
            # Get user from database (Async)
            user = await AuthService.get_user_by_id(db, user_id)
            if user is None:
                logger.warning(f"Refresh token invalid: User ID {user_id} not found.")
                return None
            if not user.is_active:
                 logger.warning(f"Refresh token invalid: User ID {user_id} is inactive.")
                 return None
                
            # Create new access token (Sync)
            access_token = create_access_token(user)
            
            # Ensure UserResponse expects model or adapt it
            user_response = UserResponse(
                 id=user.id,
                 email=user.email,
                 full_name=user.full_name,
                 role=user.role
            )
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token, # Usually return the same refresh token
                token_type="bearer",
                user=user_response
            )
        except Exception as e: # Catch potential decoding errors too
             logger.error(f"Error refreshing token: {e}", exc_info=True)
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
        existing_user = await AuthService.get_user_by_email(None, user_data.email)
        if existing_user is not None:
            return None
            
        # In a real implementation, we would create a new user in the database
        # For now, we'll just return a mock response
        new_user = {
            "id": str(secrets.randbelow(1000000)),
            "email": user_data.email,
            "password_hash": AuthService.get_password_hash(user_data.password),
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