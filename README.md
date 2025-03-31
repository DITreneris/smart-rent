# SmartRent

A decentralized property rental platform built on blockchain technology.

![Version](https://img.shields.io/badge/version-0.5.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

SmartRent connects property owners with potential renters through a secure, transparent blockchain platform. The application streamlines the rental process from property listing to contract completion, with secure payments and verifiable property history.

## Current Status (v0.5.0 - April 2025)

SmartRent is currently in active development with the following features implemented:

- ✅ Web3 wallet connection and authentication
- ✅ Property listing and management
- ✅ Smart contract integration
- ✅ Comprehensive error handling
- ✅ Blockchain event listeners
- ✅ CI/CD pipeline
- 🔄 Transaction monitoring (In Progress)
- 🔄 Database migrations (In Progress)

See our [Development Plan](./dev_plan.md) for detailed information about our progress and roadmap.

## Features

- **Property Management**: List, browse, and manage properties
- **Web3 Integration**: Connect with MetaMask and other Ethereum wallets
- **Smart Contracts**: Secure rental agreements on Ethereum blockchain
- **User Dashboards**: Dedicated interfaces for property owners and renters
- **Transaction Tracking**: Monitor and verify blockchain transactions

## Tech Stack

### Frontend
- React with TypeScript
- Ethers.js for blockchain interactions
- CSS modules and TailwindCSS

### Backend
- FastAPI
- MongoDB
- Web3 event listeners

### Smart Contracts
- Solidity
- OpenZeppelin
- Hardhat

## Development

### Prerequisites
- Node.js (v16+)
- Python (v3.9+)
- MongoDB
- Ethereum development environment (Hardhat)

### Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/smart-rent.git
cd smart-rent
```

2. Install dependencies
```bash
# Frontend
cd frontend
npm install

# Backend
cd ../backend
pip install -r requirements.txt
```

3. Set up environment variables
```bash
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env
```

4. Run the development servers
```bash
# Frontend
cd frontend
npm run dev

# Backend
cd ../backend
uvicorn app.main:app --reload
```

5. Run tests
```bash
# Frontend
cd frontend
npm test

# Backend
cd ../backend
pytest
```

## Testing

The project has a comprehensive testing infrastructure with:

- Unit tests for utility functions and components
- Integration tests for API endpoints
- Smart contract tests for blockchain interactions
- End-to-end tests for critical user flows

See the [Testing Strategy](./dev_plan.md#testing-strategy) section in our development plan for more details.

## Deployment

SmartRent uses GitHub Actions for continuous integration and deployment:

- **Development**: Automatic testing and staging deployment from the `develop` branch
- **Production**: Manual approval workflow for deploying to production from the `main` branch

## Roadmap

See our [ROADMAP.md](./ROADMAP.md) for detailed information about upcoming features and milestones.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please refer to our [Code Review Process](./dev_plan.md#review-process) before submitting your PR.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Project Link: [https://github.com/yourusername/smart-rent](https://github.com/yourusername/smart-rent) 