# SmartRent

SmartRent is a decentralized property rental platform built on blockchain technology.

![Version](https://img.shields.io/badge/version-0.5.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

SmartRent connects property owners with potential renters through a secure, transparent blockchain platform. The application streamlines the rental process from property listing to contract completion, with secure payments and verifiable property history.

## Current Status (v0.5.0 - April 2025)

SmartRent is currently in active development with the following features implemented:

- ✅ Web3 wallet connection and authentication
- ✅ Property listing and management
- ✅ JWT authentication with role-based access control
- ✅ User authentication (traditional and wallet-based)
- ✅ FastAPI application setup with middleware
- ✅ Blockchain event listeners
- ✅ CI/CD pipeline
- 🔄 Transaction monitoring (In Progress)
- 🔄 Database migrations (In Progress)

See [ROADMAP.md](./ROADMAP.md) for a comprehensive development timeline and future plans.

## Features

- **Property Management**: List, browse, and manage properties
- **Web3 Integration**: Connect with Ethereum wallets
- **Smart Contracts**: Secure rental agreements on blockchain
- **User Authentication**: Traditional and wallet-based authentication
- **Transaction Tracking**: Monitor and verify blockchain transactions

## Technical Architecture

SmartRent is built with:

- **FastAPI** for high-performance API endpoints
- **MongoDB** for flexible data storage
- **Web3.py** for Ethereum blockchain integration
- **Hyperledger Fabric** for private chain functionality
- **JWT authentication** with refresh token support
- **Cryptocurrency network** integrations

## Tech Stack

### Backend
- FastAPI (Python)
- MongoDB
- Web3 event listeners

### Frontend (Planned)
- React with TypeScript
- Ethers.js for blockchain interactions
- Material UI components

### Smart Contracts
- Solidity
- OpenZeppelin
- Hardhat

## Getting Started

### Prerequisites

- Python 3.9+
- MongoDB
- Ethereum node (or testnet connection)
- Hyperledger Fabric network (optional for development)

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
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application
```bash
python -m app.main
```

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

The project has a comprehensive testing framework:

- Unit tests for utility functions and services
- Integration tests for API endpoints
- Smart contract tests for blockchain interactions

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

Last Updated: April, 2025
Version: 0.5.2 
  