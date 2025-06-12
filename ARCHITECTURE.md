# SmartRent Platform Architecture

## Overview

SmartRent is a blockchain-enhanced property rental platform using modern web technologies. The MVP focuses on core rental flows leveraging a single EVM-compatible blockchain for minimal on-chain anchoring (e.g., metadata storage or event emission) combined with an off-chain backend and database for primary business logic and data management.

## System Architecture

### 1. Frontend Layer
- React with TypeScript
- Web3 integration via ethers.js
- Material-UI components
- Redux for state management
- Progressive Web App (PWA) support

### 2. Backend Layer
- FastAPI (Python) for REST API
- Asynchronous request handling
- JWT-based authentication
- Rate limiting with Redis
- Google OAuth integration

### 3. Database Layer
- MongoDB Atlas for document storage
- Collections:
  - properties
  - users
  - contracts
  - proposals
  - property_photos
  - documents
- Indexes for efficient querying
- GDPR-compliant data storage

### 4. Blockchain Layer (MVP)
- **Technology:** EVM-compatible blockchain (e.g., Ethereum, Polygon)
- **Contract:** `SmartRent.sol` (Solidity)
- **Role:** Minimal on-chain functions for the MVP. Primarily used for:
    - Anchoring key data references (e.g., metadata URIs for properties/agreements).
    - Potentially emitting events for significant state changes (e.g., `RentalConfirmed`).
- **Interaction:** Primarily managed via the backend service interacting with deployed contract(s).

### 5. Authentication System
- Multi-factor authentication:
  - Google OAuth
  - Wallet signatures
- JWT token management
- Session handling
- Role-based access control

## Service Architecture

### Core Services (Located within `app` directory)

1. **Property Service**
```python
class PropertyService:
    """Manages property listings and operations (primarily off-chain)."""
    - create_property()
    - update_property()
    - list_properties()
    - search_properties()
```

2. **Transaction Service / Monitor**
```python
class TransactionMonitor:
    """Handles monitoring of relevant on-chain transactions (single chain)."""
    - monitor_transaction() # Monitors specific transactions on the EVM chain
    # - verify_cross_chain() # Removed for MVP
    - process_transaction_batch() # If needed for batch processing
```

3. **Authentication Service**
```python
class MultiFactorAuth:
    """Manages user authentication."""
    - verify_google_token()
    - verify_wallet_signature()
    - create_session()
```

4. **Blockchain Service**
```python
class BlockchainService:
    """Handles interactions with the EVM blockchain and SmartRent contract."""
    # Minimal functions for MVP:
    - get_contract_metadata(property_id)
    - emit_rental_event(rental_data) # Example if event emission is used
    # - submit_transaction() # If needed for simple state changes
    # - verify_transaction() # Basic verification on the single chain
```

## Data Flow

1. **Property Listing Flow (MVP Example)**
```mermaid
graph TD
    A[Landlord] -->|Creates Listing| B[Frontend]
    B -->|Validates| C[Backend API (`app`)]
    C -->|Stores Details| D[MongoDB]
    C -->|Optionally Anchors Metadata| E[Smart Contract (via Backend)]
```

2. **Rental Process Flow (MVP Example - Off-chain focus)**
```mermaid
graph TD
    A[Tenant] -->|Submits Proposal| B[Frontend]
    B -->|Validates| C[Backend API]
    C -->|Creates| D[Proposal Document (MongoDB)]
    C -->|Updates State Off-chain| F[Backend Logic/DB]
    F -->|Optionally Emits Event| E[Smart Contract (via Backend)]
```

## Security Architecture

### 1. Authentication Security
- Multi-factor authentication
- JWT token encryption
- Wallet signature verification
- Session management

### 2. Data Security
- MongoDB Atlas security features
- Encrypted data storage
- GDPR compliance
- Data backup and recovery

### 3. API Security
- Rate limiting
- CORS protection
- Input validation
- Request sanitization

### 4. Blockchain Security
- Smart contract auditing (Essential for any on-chain logic)
- Transaction verification (On the single relevant chain)
# - Cross-chain validation # Removed for MVP
- Access controls for contract functions

## Infrastructure

### Development Environment
```yaml
services:
  api: # Located in 'app' directory
    # FastAPI service
    - Port: 8000
    - Environment: Python 3.9+
    
  frontend:
    # React development server
    - Port: 3000
    - Environment: Node.js 16+
    
  redis:
    # Caching and rate limiting
    - Port: 6379
    
  # hyperledger: # Removed for MVP
  #   # Fabric network
  #   - Ports: 7051, 7054
```

### Production Environment
- Containerized deployment
- Load balancing
- Auto-scaling
- Health monitoring
- Automated backups

## Monitoring and Logging

### System Monitoring
- API performance metrics
- Database query monitoring
- Blockchain transaction tracking
- Error rate monitoring

### Transaction Monitoring
- Payment confirmation (If applicable to MVP)
- Contract state updates (If applicable to MVP)

### User Analytics
- User engagement metrics
- Feature usage tracking
- Performance monitoring
- Error tracking

## Development Workflow

### 1. Code Management
- Git version control
- Feature branch workflow
- Pull request reviews
- Automated testing

### 2. CI/CD Pipeline
- Automated builds
- Test execution
- Code quality checks
- Deployment automation

### 3. Testing Strategy
- Unit tests
- Integration tests
- End-to-end tests
- Smart contract tests

## Future Enhancements

1. **Scalability**
   - Horizontal scaling
   - Database sharding
   - Caching optimization
   - Load balancing

2. **Features**
   - Advanced search
   - Real-time notifications
   - Dispute resolution
   - Analytics dashboard

3. **Integration**
   - Additional payment methods
   - External services
   - Mobile applications
   - API marketplace

---

Last Updated: [Insert Current Date] - MVP Refocus
Version: 0.6.0 (MVP Branch) 