# Docker Setup for Smart Rent Platform

This document provides instructions for setting up and running the Smart Rent Platform using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git (for cloning the repository)

## Project Structure

The Smart Rent Platform consists of several components, each running in its own Docker container:

- **Frontend**: React application served by Nginx
- **Backend**: FastAPI application
- **Database**: PostgreSQL database
- **Ethereum Node**: Local Hardhat node for blockchain development

## Development Environment

### Starting the Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/smart-rent-platform.git
   cd smart-rent-platform
   ```

2. Create required environment files (copying from examples):
   ```bash
   cp backend/.env.example backend/.env.docker
   cp frontend/.env.example frontend/.env.docker
   ```

3. Start the development environment:
   ```bash
   docker-compose up
   ```

This will start all services in development mode with hot-reloading enabled:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Ethereum Node: http://localhost:8545
- Database Admin: http://localhost:8080

### Development Workflow

- Frontend and backend code changes will be automatically detected and hot-reloaded
- The local Ethereum node will persist blockchain state as long as the container is not removed
- Database changes are persisted in a Docker volume

## Production Environment

### Setting Up Production

1. Create production environment files:
   ```bash
   cp backend/.env.prod.example backend/.env.prod
   ```

2. Edit the production environment files with your actual production values.

3. (Optional) Set up SSL certificates:
   ```bash
   mkdir -p ssl
   # Copy your SSL certificates into the ssl directory
   ```

4. Start the production environment:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

This will start all services in production mode:
- Frontend+Backend: http://your-domain.com (or https if SSL is configured)

### Production Configuration

The production setup includes:
- Gunicorn for serving the backend with multiple workers
- Nginx for serving the frontend and handling SSL termination
- Automatic restarts for all services

## Environment Variables

### Frontend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| REACT_APP_API_URL | Backend API URL | http://localhost/api/v1 |
| REACT_APP_ETHEREUM_NETWORK | Ethereum network to connect to | localhost |
| REACT_APP_ETHEREUM_CHAIN_ID | Ethereum chain ID | 1337 |
| REACT_APP_ETHEREUM_RPC_URL | Ethereum RPC URL | http://localhost:8545 |
| REACT_APP_RENTAL_CONTRACT_ADDRESS | Address of the deployed rental contract | 0x... |

### Backend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://postgres:postgres@db:5432/smartrent |
| SECRET_KEY | JWT secret key | your_secret_key |
| ALGORITHM | JWT algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | JWT token expiry | 60 |
| CORS_ORIGINS | Allowed CORS origins | http://localhost,http://localhost:3000 |
| ETHEREUM_NODE_URL | Ethereum node URL | http://hardhat:8545 |
| ETHEREUM_CHAIN_ID | Ethereum chain ID | 1337 |

## Container Management

### Viewing Logs

```bash
# View logs for all services
docker-compose logs

# View logs for a specific service
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f
```

### Executing Commands in Containers

```bash
# Run a command in the backend container
docker-compose exec backend python -m pytest

# Run a command in the frontend container
docker-compose exec frontend npm test

# Run a bash shell in a container
docker-compose exec backend bash
```

### Database Management

The database data is persisted in a Docker volume. You can manage it using:

```bash
# List volumes
docker volume ls

# Backup the database
docker-compose exec db pg_dump -U postgres smartrent > backup.sql

# Restore the database
cat backup.sql | docker-compose exec -T db psql -U postgres smartrent
```

## Deployment

### Building for Production

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Push images to a registry
docker-compose -f docker-compose.prod.yml push
```

### Deploying to a Server

1. Transfer the `docker-compose.prod.yml` file and environment files to your server.
2. Pull the Docker images:
   ```bash
   docker-compose -f docker-compose.prod.yml pull
   ```
3. Start the services:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Troubleshooting

### Common Issues

- **Container fails to start**: Check the logs for that specific container.
- **Network connectivity issues**: Ensure all services can communicate with each other.
- **Database connection errors**: Verify the database connection string and credentials.
- **Frontend cannot connect to backend**: Check CORS settings and API URL.

### Container Health Checks

The Docker Compose files include health checks for critical services like the database. You can check their status with:

```bash
docker-compose ps
```

## Customization

### Adding New Services

To add a new service to the Docker Compose setup:

1. Add the service definition to the Docker Compose files
2. Create a Dockerfile for the service
3. Configure any required environment variables
4. Update the network configuration if needed

### Modifying Existing Services

To modify an existing service:

1. Edit the Dockerfile or Docker Compose service definition
2. Rebuild the affected containers:
   ```bash
   docker-compose up -d --build <service-name>
   ```

## Security Considerations

- Never commit sensitive environment variables to version control
- Use secure passwords for the database and other services
- Enable HTTPS in production
- Regularly update base Docker images and dependencies
- Implement proper authentication and authorization 