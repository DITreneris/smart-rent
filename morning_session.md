# SmartRent Morning Coding Session Plan

## Session Overview
**Date:** April 2025  
**Duration:** 3-4 hours  
**Focus:** Critical Web3 integration and backend authentication

## Top 5 Priorities for Today

### Priority 1: Implement TransactionMonitoringService ✅

**Goal:** Create the foundation for monitoring transactions across networks to ensure payment integrity

**Tasks:**
1. Create basic service structure
   - [x] Set up TransactionMonitoringService class
   - [x] Implement constructor with required dependencies
   - [x] Add configuration options for polling intervals

2. Implement core monitoring logic
   - [x] Create monitor_transaction method
   - [x] Set up transaction status checking
   - [x] Implement polling mechanism with asyncio
   - [x] Add transaction state tracking

3. Add transaction result handling
   - [x] Implement success callback system
   - [x] Create failure handling with retry logic
   - [x] Add logging for transaction states
   - [x] Implement timeout handling

4. Write basic unit tests
   - [ ] Test transaction polling mechanism
   - [ ] Test success handling
   - [ ] Test failure and retry logic
   - [ ] Test timeout scenarios

**Status:** Completed main implementation of TransactionMonitoringService in app/services/transaction_monitoring.py with full monitoring capabilities. Tests pending.

### Priority 2: Set up Authentication and Authorization ✅

**Goal:** Implement secure user authentication and role-based access control for API endpoints

**Tasks:**
1. Set up JWT authentication system
   - [x] Create JWT token generation function
   - [x] Implement token validation mechanism
   - [x] Add refresh token functionality
   - [x] Set up proper token expiration

2. Build authentication middleware
   - [x] Create FastAPI dependency for auth
   - [x] Implement token extraction from requests
   - [x] Add user identification logic
   - [x] Set up role determination

3. Implement role-based authorization
   - [x] Define user roles (tenant, landlord, admin)
   - [x] Create permission verification system
   - [x] Implement role enforcement on endpoints
   - [x] Add proper error responses for unauthorized requests

4. Connect auth to frontend
   - [ ] Set up auth state management in frontend
   - [ ] Implement token storage mechanism
   - [ ] Add login/logout functionality
   - [ ] Create auth interceptor for API requests

**Status:** Completed backend authentication system with JWT tokens, refresh tokens, role-based access control, and necessary API endpoints. Frontend integration pending.

### Priority 3: Implement API Endpoints for Properties ✅

**Goal:** Create RESTful API endpoints for property listing and management

**Tasks:**
1. Design property API routes
   - [x] Plan endpoint structure and naming conventions
   - [x] Define request/response models with Pydantic
   - [x] Map out required query parameters
   - [x] Document endpoint behaviors

2. Implement CRUD operations for properties
   - [x] Create property listing endpoint (POST /api/properties)
   - [x] Implement property retrieval (GET /api/properties/{id})
   - [x] Add property update functionality (PUT /api/properties/{id})
   - [x] Implement property deletion (DELETE /api/properties/{id})

3. Add search and filtering
   - [x] Implement property listing with filters (GET /api/properties)
   - [x] Add pagination support
   - [x] Create sorting options
   - [x] Implement search functionality

4. Connect to MongoDB service layer
   - [x] Ensure property service integration
   - [x] Implement transaction handling
   - [x] Add proper error handling
   - [x] Optimize query performance

**Status:** Completed full property API endpoints with CRUD operations, search functionality, pagination, and proper authentication integration.

### Priority 4: Implement Receipt Generation

**Goal:** Create system for generating transaction receipts and payment confirmations

**Tasks:**
1. Design receipt data model
   - [ ] Define receipt structure and fields
   - [ ] Create MongoDB schema for receipts
   - [ ] Add relations to properties and users
   - [ ] Design receipt status tracking

2. Implement receipt generation service
   - [ ] Create ReceiptService class
   - [ ] Implement generate_receipt method
   - [ ] Add verification signature
   - [ ] Connect to blockchain transaction data

3. Create receipt storage and retrieval
   - [ ] Implement receipt storage in MongoDB
   - [ ] Add receipt query methods
   - [ ] Create receipt history functionality
   - [ ] Implement receipt verification

4. Add PDF generation capability
   - [ ] Set up PDF template system
   - [ ] Implement PDF generation function
   - [ ] Add branding and styling
   - [ ] Include verification QR code

### Priority 5: Begin ML Data Pipeline Design

**Goal:** Design the initial architecture for ML data collection and processing

**Tasks:**
1. Define data requirements
   - [ ] Identify required data points for property pricing
   - [ ] List external data sources
   - [ ] Define data schemas and formats
   - [ ] Create data collection plan

2. Design initial pipeline architecture
   - [ ] Sketch data flow diagram
   - [ ] Identify processing stages
   - [ ] Select appropriate tools/frameworks
   - [ ] Define storage requirements

3. Plan data preprocessing workflow
   - [ ] List required data cleaning steps
   - [ ] Design feature extraction approach
   - [ ] Identify data transformation needs
   - [ ] Plan data validation checks

4. Create initial ML model structure
   - [ ] Research appropriate algorithms for pricing
   - [ ] Define feature importance analysis process
   - [ ] Plan model training approach
   - [ ] Design model evaluation framework

## Progress Summary

We have successfully completed the top three priorities:

1. **Transaction Monitoring Service** - Implemented the full service with monitoring capabilities, confirmation handling, and error management.

2. **Authentication and Authorization System** - Created a complete JWT-based authentication system with:
   - Token generation and validation in app/auth/jwt.py
   - Role-based authorization dependencies in app/auth/dependencies.py
   - Authentication service and endpoints for login, registration, and token refresh

3. **Property API Endpoints** - Implemented RESTful API for property management with:
   - CRUD operations for properties
   - Search functionality with filtering
   - Proper authorization protection
   - MongoDB integration

Next steps will focus on implementing the Receipt Generation system and beginning the ML Data Pipeline design.

## Detailed Implementation Steps

### TransactionMonitoringService Implementation

1. **Initial Setup**
```python
# app/services/transaction_monitoring.py

import asyncio
from typing import Dict, Callable, Optional
from app.providers.web3 import Web3Provider
from app.providers.hyperledger import HyperledgerClient
from app.providers.crypto import CryptoNetworkClient
from app.config import settings

class TransactionMonitoringService:
    """Service for monitoring transactions across networks."""
    
    def __init__(self):
        self.web3 = Web3Provider()
        self.fabric_client = HyperledgerClient()
        self.crypto_client = CryptoNetworkClient()
        self.polling_interval = settings.TX_POLLING_INTERVAL
        self.max_attempts = settings.TX_MAX_ATTEMPTS
        self.active_transactions = {}
```

2. **Core Monitoring Logic**
```python
# Continue in app/services/transaction_monitoring.py

async def monitor_transaction(self, tx_hash: str, on_success: Optional[Callable] = None, 
                             on_failure: Optional[Callable] = None):
    """Monitor transaction status across networks."""
    
    # Register transaction as active
    self.active_transactions[tx_hash] = {
        "status": "pending",
        "attempts": 0,
        "last_checked": None,
        "confirmations": 0
    }
    
    # Start monitoring loop
    attempts = 0
    while attempts < self.max_attempts:
        try:
            # Update transaction record
            self.active_transactions[tx_hash]["attempts"] = attempts
            self.active_transactions[tx_hash]["last_checked"] = datetime.now()
            
            # Check status
            status = await self.web3.get_transaction_status(tx_hash)
            
            # Handle confirmation
            if status.confirmed:
                await self._handle_confirmation(tx_hash)
                if on_success:
                    await on_success(tx_hash)
                return True
                
            # Sleep before next check
            attempts += 1
            await asyncio.sleep(self.polling_interval)
            
        except Exception as e:
            self.active_transactions[tx_hash]["status"] = "error"
            self.active_transactions[tx_hash]["error"] = str(e)
            
            if on_failure:
                await on_failure(tx_hash, str(e))
            return False
    
    # Handle timeout
    self.active_transactions[tx_hash]["status"] = "timeout"
    if on_failure:
        await on_failure(tx_hash, "Transaction monitoring timed out")
    return False
```

3. **Handle Confirmations and Verification**
```python
# Continue in app/services/transaction_monitoring.py

async def _handle_confirmation(self, tx_hash: str):
    """Handle transaction confirmation and verification."""
    
    # Update status
    self.active_transactions[tx_hash]["status"] = "confirming"
    
    # Verify across networks
    verification_result = await self._verify_across_networks(tx_hash)
    
    if verification_result.success:
        self.active_transactions[tx_hash]["status"] = "verified"
        await self._update_contract_state(tx_hash)
    else:
        self.active_transactions[tx_hash]["status"] = "verification_failed"
        self.active_transactions[tx_hash]["verification_details"] = verification_result

async def _verify_across_networks(self, tx_hash: str):
    """Verify transaction across different networks."""
    
    # Verify on cryptocurrency network
    crypto_verified = await self.crypto_client.verify_transaction(tx_hash)
    
    # Verify on Hyperledger
    fabric_verified = await self.fabric_client.verify_transaction(tx_hash)
    
    # Combine results
    return VerificationResult(
        success=(crypto_verified and fabric_verified),
        details={
            "crypto_network": crypto_verified,
            "hyperledger": fabric_verified
        }
    )

async def _update_contract_state(self, tx_hash: str):
    """Update contract state after successful verification."""
    # Implementation details
```

### Authentication System Implementation

1. **JWT Token Generation and Validation**
```python
# app/auth/jwt.py

import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
from app.config import settings
from app.models.user import User

def create_access_token(user_data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT access token."""
    
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
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Dict:
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

2. **Authentication Middleware for FastAPI**
```python
# app/auth/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.services.user_service import UserService
from app.auth.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from JWT token."""
    
    # Decode token
    payload = decode_token(token)
    user_id = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    # Get user from database
    user = await UserService.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user

async def get_current_active_user(current_user = Depends(get_current_user)):
    """Verify user is active."""
    if not current_user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user
```

## Expected Outcomes

By the end of this morning coding session, we aim to have:

1. A functional TransactionMonitoringService that can track blockchain transactions
2. Working authentication system with JWT tokens and role-based access
3. Basic API endpoints for property management
4. Framework for receipt generation
5. Initial design for ML data pipeline architecture

These components will provide the foundation for the critical Web3 integration features needed for the SmartRent platform and prepare us for the upcoming v0.6.0 release requirements.

## Next Steps After This Session

1. Connect the TransactionMonitoringService to the frontend
2. Implement NetworkVerificationService in detail
3. Complete API endpoints for rentals
4. Add blockchain event listeners
5. Begin implementation of the data collection pipeline for property price models 