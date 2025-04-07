"""
Authentication router for user login and registration.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, Dict, Any

from app.models.auth import (
    LoginRequest, 
    RegisterRequest,
    TokenResponse, 
    RefreshTokenRequest,
    UserResponse,
    WalletAuthRequest,
    WalletNonceRequest,
    WalletNonceResponse,
    ErrorResponse
)
from app.services.auth_service import AuthService
from app.auth.dependencies import get_current_user

# Create router
router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
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
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = await AuthService.create_access_token(
        data={"sub": user["id"], "role": user["role"]}
    )
    refresh_token = await AuthService.create_refresh_token(user["id"])
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": UserResponse(
            id=user["id"],
            email=user.get("email"),
            full_name=user.get("full_name"),
            role=user["role"],
            wallet_address=user.get("wallet_address")
        )
    }

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, response: Response):
    """
    Login with email and password.
    """
    token_response = await AuthService.login(login_data)
    if token_response is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Set cookies for web clients
    response.set_cookie(
        key="access_token",
        value=token_response.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600  # 1 hour
    )
    response.set_cookie(
        key="refresh_token",
        value=token_response.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800  # 7 days
    )
    
    return token_response

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: RegisterRequest):
    """
    Register a new user.
    """
    user = await AuthService.register(user_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    
    return user

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_data: RefreshTokenRequest, response: Response):
    """
    Refresh the access token using a refresh token.
    """
    token_response = await AuthService.refresh_token(refresh_data.refresh_token)
    if token_response is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update cookies for web clients
    response.set_cookie(
        key="access_token",
        value=token_response.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600  # 1 hour
    )
    
    return token_response

@router.post("/wallet/nonce", response_model=WalletNonceResponse)
async def get_wallet_nonce(request: WalletNonceRequest):
    """
    Get a nonce for wallet-based authentication.
    """
    # Generate a nonce for the wallet address
    nonce = await AuthService.generate_nonce(request.address)
    message = f"Login to SmartRent: {nonce}"
    
    return WalletNonceResponse(
        nonce=nonce,
        message=message
    )

@router.post("/wallet/login", response_model=TokenResponse)
async def login_with_wallet(wallet_data: WalletAuthRequest, response: Response):
    """
    Login with a wallet signature.
    """
    token_response = await AuthService.login_with_wallet(
        wallet_data.address,
        wallet_data.message,
        wallet_data.signature
    )
    
    if token_response is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Set cookies for web clients
    response.set_cookie(
        key="access_token",
        value=token_response.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600  # 1 hour
    )
    response.set_cookie(
        key="refresh_token",
        value=token_response.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800  # 7 days
    )
    
    return token_response

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get information about the currently authenticated user.
    """
    return UserResponse(
        id=current_user["id"],
        email=current_user.get("email"),
        full_name=current_user.get("full_name"),
        role=current_user["role"],
        wallet_address=current_user.get("wallet_address")
    )

@router.post("/logout")
async def logout(response: Response):
    """
    Logout the user by clearing auth cookies.
    """
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    
    return {"detail": "Successfully logged out"} 