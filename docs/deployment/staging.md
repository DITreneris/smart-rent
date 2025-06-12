# Staging Deployment

This guide covers deploying SmartRent to a staging environment. The staging environment should mirror the production environment as closely as possible, but is used for testing changes before they go to production.

## Prerequisites

- A server or cloud instance (e.g., AWS EC2, DigitalOcean Droplet)
- Docker and Docker Compose installed
- Domain name configured for staging (e.g., staging.smartrent.com)
- GitHub access to the SmartRent repository
- SSL certificate for the staging domain

## Step 1: Server Setup

### Provision Server

For AWS EC2:
```bash
# Example using AWS CLI
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.medium \
    --key-name your-key-pair \
    --security-group-ids sg-0123456789abcdef0
```

Or use the cloud provider's web console to create a server with:
- Ubuntu 20.04 LTS
- At least 2 GB RAM
- 20 GB storage
- Proper security groups/firewall settings

### Connect to Server

```bash
ssh user@your-server-ip
```

### Update Server

```bash
sudo apt update
sudo apt upgrade -y
```

### Install Docker and Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ${USER}
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Step 2: Clone Repository

```bash
git clone https://github.com/DITreneris/smart-rent.git
cd smart-rent

# Checkout the staging branch if exists, otherwise use main
git checkout staging 2>/dev/null || git checkout main
```

## Step 3: Configure Environment

Create `.env` file for staging:

```bash
cp .env.example .env.staging
```

Edit `.env.staging` with appropriate values:

```env
# Basic settings
ENVIRONMENT=staging
DEBUG=False
SECRET_KEY=generate-a-secure-key
JWT_SECRET=generate-a-secure-jwt-secret

# Database settings
MONGO_CONNECTION_STRING=mongodb://mongo:27017/
MONGO_DB_NAME=smartrent_staging

# Web3 settings
WEB3_PROVIDER_URL=your-staging-web3-provider
CONTRACT_ADDRESS=your-staging-contract-address

# Redis settings
REDIS_HOST=redis
REDIS_PORT=6379

# Admin user
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=secure-password
ADMIN_FULL_NAME=Admin User

# Hosts settings
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=https://staging.smartrent.com
```

## Step 4: Create Docker Compose Configuration

Create or modify `docker-compose.staging.yml`:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    restart: always
    ports:
      - "8000:8000"
    depends_on:
      - mongo
      - redis
    env_file:
      - .env.staging
    volumes:
      - ./uploads:/app/uploads
    networks:
      - smartrent-network

  mongo:
    image: mongo:4.4
    restart: always
    volumes:
      - mongo-data:/data/db
    networks:
      - smartrent-network

  redis:
    image: redis:6.0
    restart: always
    volumes:
      - redis-data:/data
    networks:
      - smartrent-network

  nginx:
    image: nginx:latest
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/staging.conf:/etc/nginx/conf.d/default.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./static:/var/www/static
    depends_on:
      - app
    networks:
      - smartrent-network

networks:
  smartrent-network:

volumes:
  mongo-data:
  redis-data:
```

## Step 5: Configure Nginx

Create `nginx/staging.conf`:

```bash
mkdir -p nginx
```

```nginx
server {
    listen 80;
    server_name staging.smartrent.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name staging.smartrent.com;

    ssl_certificate /etc/nginx/ssl/staging.smartrent.com.crt;
    ssl_certificate_key /etc/nginx/ssl/staging.smartrent.com.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;

    location /static/ {
        alias /var/www/static/;
        expires 30d;
    }

    location /api/ {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Step 6: Add SSL Certificates

Place your SSL certificates in the `nginx/ssl` directory:

```bash
mkdir -p nginx/ssl
# Copy your SSL certificates to this directory
# For example:
# scp local/path/to/certificate.crt user@your-server-ip:~/smart-rent/nginx/ssl/staging.smartrent.com.crt
# scp local/path/to/private.key user@your-server-ip:~/smart-rent/nginx/ssl/staging.smartrent.com.key
```

## Step 7: Build and Deploy

```bash
# Build and start the containers
docker-compose -f docker-compose.staging.yml up -d

# Check logs
docker-compose -f docker-compose.staging.yml logs -f
```

## Step 8: Initial Configuration

### Create Admin User

```bash
# Connect to the app container
docker-compose -f docker-compose.staging.yml exec app python -m scripts.create_admin
```

### Initialize Database

```bash
# Connect to the app container
docker-compose -f docker-compose.staging.yml exec app python -m scripts.init_db
```

## Step 9: Continuous Deployment Setup

For automatic deployments from GitHub, you can set up GitHub Actions.

Create `.github/workflows/deploy-staging.yml`:

```yaml
name: Deploy to Staging

on:
  push:
    branches:
      - develop  # Or your staging branch

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up SSH
        uses: webfactory/ssh-agent@v0.5.3
        with:
          ssh-private-key: ${{ secrets.STAGING_SSH_KEY }}

      - name: Deploy to staging
        run: |
          ssh -o StrictHostKeyChecking=no ${{ secrets.STAGING_SSH_USER }}@${{ secrets.STAGING_SSH_HOST }} << 'EOF'
            cd smart-rent
            git pull
            docker-compose -f docker-compose.staging.yml down
            docker-compose -f docker-compose.staging.yml up -d --build
          EOF
```

## Maintenance

### Viewing Logs

```bash
docker-compose -f docker-compose.staging.yml logs -f
```

### Updating Deployment

```bash
# Pull latest changes
git pull

# Rebuild and restart containers
docker-compose -f docker-compose.staging.yml down
docker-compose -f docker-compose.staging.yml up -d --build
```

### Backup Database

```bash
# Create backup directory
mkdir -p backups

# Backup MongoDB
docker-compose -f docker-compose.staging.yml exec mongo mongodump --out=/data/db/backup
docker cp $(docker-compose -f docker-compose.staging.yml ps -q mongo):/data/db/backup ./backups/mongodb-$(date +%Y%m%d)
```

## Troubleshooting

### Container Issues

```bash
# Check container status
docker-compose -f docker-compose.staging.yml ps

# Restart a specific service
docker-compose -f docker-compose.staging.yml restart app

# View logs for a specific service
docker-compose -f docker-compose.staging.yml logs app
```

### Database Connection Issues

```bash
# Check MongoDB connection
docker-compose -f docker-compose.staging.yml exec app python -c "from app.core.mongo_db import db; print(db.client.server_info())"
```

### SSL Certificate Issues

```bash
# Check Nginx configuration
docker-compose -f docker-compose.staging.yml exec nginx nginx -t
``` 