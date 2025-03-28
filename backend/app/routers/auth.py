from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os
from functools import lru_cache
import time

from .. import models
from ..database import get_db
from ..schemas import auth as auth_schemas
from app.contracts.users import get_user_by_username, get_user_by_id, create_user, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={401: {"description": "Unauthorized"}},
)

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Token blacklist for logged out tokens
token_blacklist = set()

# Access token version cache to ensure tokens are invalidated when password changes
# Format: {user_id: token_version}
token_version_cache = {}

# Create or update token_version when user changes password
def update_token_version(user_id: int):
    token_version_cache[user_id] = time.time()

# Get the current token version for a user
def get_token_version(user_id: int) -> float:
    return token_version_cache.get(user_id, 0)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

@lru_cache(maxsize=128)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new JWT token with expiration"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Add token version to prevent use after password change
    if "sub" in to_encode:
        user_id = int(to_encode["sub"])
        to_encode["ver"] = get_token_version(user_id)
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate the token and return the current user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Check if token is in blacklist
    if token in token_blacklist:
        raise credentials_exception
    
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # Get token version and check if it matches the current version
        token_ver = payload.get("ver", 0)
        current_ver = get_token_version(int(user_id))
        
        if token_ver < current_ver:
            # Token was issued before password change
            raise credentials_exception
        
        token_data = auth_schemas.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = await get_user_by_id(int(token_data.user_id))
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user = Depends(get_current_user)):
    """Check if the current user is active"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user

@router.post("/register", response_model=auth_schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: auth_schemas.UserCreate):
    """
    Register a new user with username and password.
    
    Returns the created user without the password.
    """
    # Check if username already exists
    existing_user = await get_user_by_username(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    try:
        new_user = await create_user(user_data)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

@router.post("/token", response_model=auth_schemas.Token)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Authenticate user and provide JWT token.
    
    - **username**: Username for authentication
    - **password**: Password for authentication
    """
    # Authenticate the user
    user = await get_user_by_username(form_data.username)
    if not user or not await verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    # Set cookie for enhanced security
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=os.getenv("ENVIRONMENT") == "production"
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
    token: str = Depends(oauth2_scheme)
):
    """
    Logout the current user by adding their token to the blacklist.
    
    Also clears the authentication cookie.
    """
    # Add token to blacklist
    token_blacklist.add(token)
    
    # Clear cookie
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=os.getenv("ENVIRONMENT") == "production"
    )
    
    return {"detail": "Successfully logged out"}

@router.get("/me", response_model=auth_schemas.UserResponse)
async def read_current_user(current_user = Depends(get_current_active_user)):
    """Get details of the currently authenticated user."""
    return current_user

@router.post("/register/tenant", response_model=auth_schemas.UserResponse)
async def register_tenant(user: auth_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=models.UserRole.TENANT,
        status=models.UserStatus.PENDING
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/register/landlord", response_model=auth_schemas.UserResponse)
async def register_landlord(user: auth_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=models.UserRole.LANDLORD,
        status=models.UserStatus.PENDING
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/me", response_model=auth_schemas.UserResponse)
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@router.put("/users/me", response_model=auth_schemas.UserResponse)
async def update_user(
    user_update: auth_schemas.UserUpdate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    if user_update.wallet_address:
        current_user.wallet_address = user_update.wallet_address
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/users/documents", response_model=auth_schemas.UserResponse)
async def upload_user_documents(
    documents: auth_schemas.DocumentUpload,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # In a real implementation, this would handle file uploads to S3
    # For now, we'll just update the document URLs in the user record
    current_user.documents = documents.document_urls
    
    db.commit()
    db.refresh(current_user)
    return current_user 