# Smart Rent Platform Contracts

This directory contains the Solidity smart contracts used by the Smart Rent Platform.

## RentalAgreement.sol

The main contract that handles rental agreements between tenants and landlords. It includes functionality for:

- Creating a new rental agreement
- Paying rent and security deposits
- Terminating or completing agreements
- Returning security deposits
- Retrieving agreement details

## Compiling Contracts

To compile the Solidity contracts, you need to have Solidity installed. You can use the Solidity compiler (`solc`) or a development framework like Truffle or Hardhat.

### Using solc directly

```bash
# Install solc
npm install -g solc

# Compile the contract
solc --optimize --abi --bin RentalAgreement.sol -o build/
```

This will generate `.abi` and `.bin` files in the `build/` directory that can be used for contract deployment.

### Using Hardhat (recommended)

```bash
# Initialize a new Hardhat project
npm init -y
npm install --save-dev hardhat @nomiclabs/hardhat-ethers ethers

# Create a hardhat.config.js file
# Run Hardhat compile
npx hardhat compile
```

## Deployment

To deploy the compiled contracts, you can use the `blockchain.py` service in the `app/services` directory. This service handles contract deployment and interaction using Web3.py.

### Prerequisites

- An Ethereum node URL (can be a testnet like Sepolia or a local node)
- A private key with sufficient ETH for gas fees
- Compiled contract ABI and bytecode

### Configuration

Update the `.env` file with the following variables:

```
ETHEREUM_NODE_URL=https://sepolia.infura.io/v3/your-project-id
ETHEREUM_PRIVATE_KEY=your-private-key
```

### Manual Deployment

You can also deploy the contract manually using tools like Remix (https://remix.ethereum.org/) or ethers.js.

## Testing

For testing the smart contracts, we recommend using Hardhat's testing framework:

```bash
npx hardhat test
```

## Security Considerations

Before deploying to mainnet, ensure that:

1. The contract has been thoroughly tested
2. Consider having a professional audit performed
3. Test on a testnet first (Sepolia, Goerli, etc.)
4. Verify the deployed contract code on Etherscan 