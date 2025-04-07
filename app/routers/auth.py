"""
Authentication router for user login and registration.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from app.models.auth import (
    TokenResponse,
    LoginRequest,
    WalletLoginRequest,
    RefreshTokenRequest,
    UserRegistrationRequest,
    WalletRegistrationRequest,
    WalletNonceResponse,
    UserResponse
)
from app.services.auth_service import AuthService
from app.auth.jwt import decode_token, verify_token_type
from app.auth.dependencies import get_current_active_user

# Create router
router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"}
    }
)

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = await AuthService.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    tokens = await AuthService.generate_tokens(user)
    return tokens

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """
    Login with username and password.
    """
    user = await AuthService.authenticate_user(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    tokens = await AuthService.generate_tokens(user)
    return tokens

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_request: RefreshTokenRequest):
    """
    Refresh access token using a refresh token.
    """
    try:
        # Decode the refresh token
        payload = decode_token(refresh_request.refresh_token)
        
        # Verify it's a refresh token
        if not verify_token_type(payload, "refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Extract user data from token
        user_data = {
            "id": payload.get("sub"),
            "role": payload.get("role", "user")
        }
        
        # Add optional fields if available
        if "email" in payload:
            user_data["email"] = payload["email"]
            
        if "wallet_address" in payload:
            user_data["wallet_address"] = payload["wallet_address"]
        
        # Generate new tokens
        tokens = await AuthService.generate_tokens(user_data)
        return tokens
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Failed to refresh token: {str(e)}"
        )

@router.post("/register", response_model=UserResponse)
async def register_user(registration_data: UserRegistrationRequest):
    """
    Register a new user.
    """
    try:
        # Register user
        user, tokens = await AuthService.register_user(
            {
                "email": registration_data.email,
                "name": registration_data.name
            },
            registration_data.password
        )
        
        # Return user data (tokens will be provided separately via login)
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/wallet/nonce", response_model=WalletNonceResponse)
async def get_wallet_nonce(wallet_address: str):
    """
    Get a nonce for wallet-based authentication.
    """
    try:
        # Generate a nonce
        nonce = AuthService.generate_wallet_connection_nonce()
        
        # In a real implementation, we would store this nonce in the database
        # with an expiration time and associate it with the wallet address
        
        # For demo purposes, we'll just return it
        expires_at = (datetime.utcnow() + timedelta(minutes=5)).isoformat()
        
        return {
            "nonce": nonce,
            "expires_at": expires_at
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to generate nonce: {str(e)}"
        )

@router.post("/wallet/login", response_model=TokenResponse)
async def wallet_login(login_data: WalletLoginRequest):
    """
    Login with a wallet signature.
    """
    try:
        user = await AuthService.authenticate_wallet(
            login_data.wallet_address,
            login_data.signature,
            login_data.nonce
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid wallet authentication"
            )
        
        tokens = await AuthService.generate_tokens(user)
        return tokens
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Wallet authentication failed: {str(e)}"
        )

@router.post("/wallet/register", response_model=UserResponse)
async def register_wallet(registration_data: WalletRegistrationRequest):
    """
    Register a new user with a wallet address.
    """
    try:
        # In a real implementation, we would:
        # 1. Check if the wallet is already registered
        # 2. Store the user data in the database
        
        # For demo purposes, we'll just return mock data
        user_id = f"user-wallet-{registration_data.wallet_address[-8:]}"
        
        user = {
            "id": user_id,
            "wallet_address": registration_data.wallet_address,
            "email": registration_data.email,
            "name": registration_data.name,
            "role": "user",
            "is_active": True
        }
        
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Wallet registration failed: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """
    Get information about the currently authenticated user.
    """
    return current_user 