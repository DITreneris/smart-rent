# Smart Rent Platform - Project Structure

## Backend

```
backend/
├── app/
│   ├── contracts/             # Smart contract source files and utilities
│   │   ├── RentalAgreement.sol  # Main rental agreement contract
│   │   └── README.md          # Compilation instructions
│   ├── models/                # Database models
│   │   ├── user.py            # User model schema
│   │   ├── property.py        # Property model schema
│   │   └── contract.py        # Contract model schema
│   ├── routers/               # API route handlers
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── properties.py      # Property management endpoints
│   │   ├── contracts.py       # Smart contract endpoints
│   │   └── admin.py           # Admin dashboard endpoints
│   ├── schemas/               # API schemas (request/response models)
│   │   ├── user.py            # User schemas
│   │   ├── property.py        # Property schemas
│   │   └── contract.py        # Contract schemas
│   ├── services/              # Business logic
│   │   ├── auth_service.py    # Authentication logic
│   │   ├── property_service.py # Property management logic
│   │   ├── contract_service.py # Contract management logic
│   │   └── blockchain.py      # Blockchain integration logic
│   ├── utils/                 # Utility functions
│   │   ├── auth.py            # Auth utilities (JWT, password handling)
│   │   └── helpers.py         # Helper functions
│   └── database.py            # Database configuration
├── tests/                     # Test suites
│   ├── test_auth.py           # Authentication tests
│   ├── test_properties.py     # Property management tests
│   ├── test_contracts.py      # Contract management tests
│   └── test_blockchain.py     # Blockchain service tests
├── requirements.txt           # Python dependencies
└── main.py                    # Application entry point
```

## Frontend

```
frontend/
├── public/                    # Static files
├── src/
│   ├── components/            # React components
│   │   ├── auth/              # Authentication components
│   │   ├── layout/            # Layout components (Navbar, Footer, etc.)
│   │   ├── properties/        # Property-related components
│   │   └── contracts/         # Contract-related components
│   ├── contexts/              # React context providers
│   │   ├── AuthContext.js     # Authentication context
│   │   └── Web3Context.js     # Web3 context (blockchain connection)
│   ├── pages/                 # Page components
│   │   ├── Home.js            # Home page
│   │   ├── Login.js           # Login page
│   │   ├── Register.js        # Registration page
│   │   ├── Dashboard.js       # User dashboard
│   │   ├── PropertyList.js    # Properties listing
│   │   └── PropertyDetail.js  # Property details
│   ├── services/              # API services
│   │   └── api.js             # API client
│   ├── store/                 # Redux store
│   │   ├── slices/            # Redux slices
│   │   │   ├── authSlice.js   # Authentication slice
│   │   │   ├── propertySlice.js # Properties slice
│   │   │   └── contractSlice.js # Contracts slice
│   │   └── index.js           # Store configuration
│   ├── styles/                # CSS styles
│   │   └── theme.css          # Theme styles
│   ├── App.js                 # Main application component
│   └── index.js               # Application entry point
├── package.json               # NPM dependencies
└── tailwind.config.js         # Tailwind CSS configuration
```

## Blockchain

The Smart Rent Platform integrates with the Ethereum blockchain through smart contracts written in Solidity. These contracts handle the following aspects:

1. **Rental Agreements** - Properties, terms, payments, termination
2. **Payment Processing** - Handling rent payments, security deposits, and refunds
3. **Contract Status Tracking** - Monitoring active vs. terminated agreements

Key blockchain components:
- `RentalAgreement.sol` - Main smart contract for managing rental agreements
- `blockchain.py` - Backend service for interacting with the smart contracts
- `Web3Context.js` - Frontend context for connecting to user's wallet and the blockchain 