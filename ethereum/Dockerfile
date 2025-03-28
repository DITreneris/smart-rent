FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy Hardhat configuration and contracts
COPY . .

# Expose port for Hardhat node
EXPOSE 8545

# Start Hardhat node
CMD ["npx", "hardhat", "node"] 