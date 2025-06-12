# SmartRent - MVP

SmartRent is a decentralized property rental platform built on blockchain technology. **This README reflects the current focus on delivering a Minimum Viable Product (MVP).**

![Version](https://img.shields.io/badge/version-0.5.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

SmartRent connects property owners with potential renters through a secure, transparent platform. The MVP focuses on streamlining the core rental process (listing, proposing, accepting) using a simplified tech stack: **React Frontend, FastAPI Backend (`app`), MongoDB, and a minimal EVM/Solidity smart contract** for on-chain anchoring/events.

## Current Status (~v0.5.x - Pre-MVP Consolidation)

SmartRent is currently undergoing consolidation and refactoring for the MVP. Key existing components include:

- ✅ Web3 wallet connection and authentication
- ✅ Property listing and management
- ✅ JWT authentication with role-based access control
- ✅ User authentication (traditional and wallet-based)
- ✅ FastAPI application setup (`app` directory) with middleware
- ✅ Basic Blockchain interaction foundations (connecting, reading)
- ✅ CI/CD pipeline (Basic)
- 🟡 **Backend Consolidation:** Merging all logic into `app` directory. (Requires manual deletion of `backend/app`)
- 🟡 **Documentation Update:** Aligning docs with MVP scope. (In Progress)
- ⬜ **MVP Rental Flow Definition:** Finalizing the core user journey.

See [ROADMAP.md](./ROADMAP.md) for the detailed MVP development plan and post-MVP features.

## MVP Features Focus

- **Property Management**: List, browse basic property details.
- **Web3 Integration**: Connect with EVM wallets (e.g., MetaMask).
- **Core Rental Flow**: Tenant proposes, Landlord accepts, state updated (primarily off-chain).
- **Smart Contracts**: Minimal on-chain anchoring/events using Solidity (e.g., storing metadata URI, emitting `RentalConfirmed`).
- **User Authentication**: Wallet-based authentication.
- **Transaction Tracking**: Basic monitoring for core flow steps on the EVM chain (if needed).

## Technical Architecture (MVP)

SmartRent MVP is built with:

- **FastAPI** (`app` directory) for high-performance API endpoints
- **MongoDB** for flexible off-chain data storage
- **Blockchain Integration:** via Web3.py (backend) / Ethers.js (frontend) for EVM chain interaction
- **JWT authentication**
- **Solidity Smart Contract** (`SmartRent.sol`) for minimal on-chain functions

## Tech Stack (MVP)

### Backend (`app` directory)
- FastAPI (Python)
- MongoDB
- Web3.py

### Frontend
- React with TypeScript
- Ethers.js for blockchain interactions
- Material UI components

### Smart Contracts
- Solidity
- Hardhat (for development/deployment)

## Getting Started (MVP Development)

### Prerequisites

- Python 3.9+
- MongoDB instance (local or Atlas)
- Node.js (for frontend development)
- EVM Testnet connection (e.g., Sepolia via Infura/Alchemy) and test ETH
- Wallet like MetaMask

### Installation

1. Clone the repository
```bash
git clone https://github.com/DITreneris/smart-rent.git
cd smart-rent
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables
```bash
# Ensure .env reflects the consolidated 'app' backend and correct endpoints/keys
cp .env.example .env 
# Edit .env with your configuration
```

4. Run the application components:
```bash
# Run Backend (from root directory)
# Ensure your environment variables are set
cd app
python -m main # Or however your main app is run (e.g., uvicorn app.main:app --reload)
cd ..

# Run Frontend (from root directory, in a separate terminal)
cd frontend
npm install
npm start
```

## API Documentation

Once the backend server (`app`) is running, access API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

The project includes frameworks for:
- Unit tests (Pytest for backend, Jest for frontend)
- Integration tests (Focusing on core API flows for MVP)
- Smart contract tests (Hardhat - if contract logic exists)

**MVP testing priority is on the core rental flow integration.**

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Project Link: [https://github.com/DITreneris/smart-rent](https://github.com/DITreneris/smart-rent)

Last Updated: [Insert Current Date] - MVP Refocus
Version: MVP Plan (Targeting v0.6.x)
  