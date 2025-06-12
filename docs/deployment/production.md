# Production Deployment

This guide covers deploying SmartRent to a production environment. Production deployment requires more rigorous security, monitoring, and reliability considerations than development or staging environments.

## Prerequisites

- Production-grade server or cloud infrastructure (e.g., AWS, Google Cloud, Azure)
- Docker and Docker Compose installed on servers
- Domain name with valid SSL certificates
- Proper monitoring tools set up
- Backup solution in place
- CI/CD pipeline configured

## Infrastructure Requirements

For a production deployment, we recommend:

- **Application Servers**: 2+ instances for high availability
- **Database**: MongoDB cluster with replication
- **Caching**: Redis cluster
- **Load Balancer**: For distributing traffic between app instances
- **Storage**: Persistent volume for uploads and static files
- **Monitoring**: Prometheus and Grafana
- **Logging**: ELK Stack or similar

## Step 1: Infrastructure Setup

### Option 1: AWS Setup

#### EC2 Instances
```bash
# Launch application server instances
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.large \
    --count 2 \
    --key-name your-key-pair \
    --security-group-ids sg-0123456789abcdef0 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=smartrent-prod-app}]'
```

#### MongoDB Atlas
- Set up a MongoDB Atlas M10+ cluster
- Configure VPC peering or appropriate network security

#### Load Balancer
```bash
# Create a load balancer
aws elbv2 create-load-balancer \
    --name smartrent-prod-lb \
    --subnets subnet-abcdef subnet-123456 \
    --security-groups sg-0123456789abcdef0 \
    --type application
```

### Option 2: Kubernetes Setup

For larger scale deployments, Kubernetes is recommended:

- Set up a Kubernetes cluster (EKS, GKE, AKS, or self-managed)
- Use Helm charts for deployment
- Set up persistent volumes for data
- Configure ingress for external access

## Step 2: Repository Setup

```bash
git clone https://github.com/DITreneris/smart-rent.git
cd smart-rent
git checkout main  # or your production branch
```

## Step 3: Production Configuration

Create `.env.production` file:

```env
# Basic settings
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=long-random-secure-key
JWT_SECRET=another-long-random-secure-key

# Database settings
MONGO_CONNECTION_STRING=mongodb+srv://username:password@your-cluster.mongodb.net/
MONGO_DB_NAME=smartrent_prod

# Web3 settings
WEB3_PROVIDER_URL=https://mainnet.infura.io/v3/your-project-id
CONTRACT_ADDRESS=0x123...

# Redis settings (if using Redis cluster)
REDIS_HOST=your-redis-cluster-endpoint
REDIS_PORT=6379

# Admin user
ADMIN_EMAIL=admin@yourcompany.com
ADMIN_PASSWORD=very-secure-password
ADMIN_FULL_NAME=Admin User

# Host settings
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=https://smartrent.com,https://www.smartrent.com
```

## Step 4: Docker Configuration

Create `docker-compose.production.yml`:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.production
    image: your-registry/smartrent:latest
    restart: always
    deploy:
      replicas: 2
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    env_file:
      - .env.production
    volumes:
      - uploads:/app/uploads
    networks:
      - smartrent-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  nginx:
    image: nginx:latest
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/production.conf:/etc/nginx/conf.d/default.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./static:/var/www/static
    depends_on:
      - app
    networks:
      - smartrent-network
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  smartrent-network:

volumes:
  uploads:
```

## Step 5: Nginx Configuration

Create `nginx/production.conf`:

```nginx
server {
    listen 80;
    server_name smartrent.com www.smartrent.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name smartrent.com www.smartrent.com;

    # SSL configuration
    ssl_certificate /etc/nginx/ssl/smartrent.com.crt;
    ssl_certificate_key /etc/nginx/ssl/smartrent.com.key;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-XSS-Protection "1; mode=block";
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' https://api.smartrent.com";

    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    # Static files
    location /static/ {
        alias /var/www/static/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    # API endpoints
    location /api/ {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90s;
        proxy_connect_timeout 90s;
        proxy_send_timeout 90s;
    }

    # Root location
    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90s;
        proxy_connect_timeout 90s;
        proxy_send_timeout 90s;
    }

    # Error pages
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
}
```

## Step 6: Production Dockerfile

Create `Dockerfile.production`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/uploads /app/static

# Collect static files
RUN python -m app.scripts.collect_static

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Step 7: Monitoring Setup

### Prometheus Configuration

Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'smartrent'
    static_configs:
      - targets: ['app:8000']
    metrics_path: '/metrics'
```

### Grafana Dashboard

- Set up Grafana dashboards for:
  - API response times
  - Error rates
  - System resource usage
  - Database performance

## Step 8: Backup Strategy

### Database Backups

Set up automated MongoDB backups:

```bash
# Create a backup script
cat << 'EOF' > /opt/backup_mongodb.sh
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/mongodb/$TIMESTAMP"

mkdir -p $BACKUP_DIR

mongodump --uri="mongodb+srv://username:password@your-cluster.mongodb.net/smartrent_prod" --out=$BACKUP_DIR

# Rotate backups (keep last 7 days)
find /backup/mongodb -type d -mtime +7 -exec rm -rf {} \;
EOF

chmod +x /opt/backup_mongodb.sh

# Add to crontab
echo "0 2 * * * /opt/backup_mongodb.sh" | crontab -
```

### File Backups

For uploaded files:

```bash
# Create a backup script
cat << 'EOF' > /opt/backup_files.sh
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/files/$TIMESTAMP"

mkdir -p $BACKUP_DIR

rsync -av /path/to/smartrent/uploads/ $BACKUP_DIR/

# Rotate backups (keep last 7 days)
find /backup/files -type d -mtime +7 -exec rm -rf {} \;
EOF

chmod +x /opt/backup_files.sh

# Add to crontab
echo "0 3 * * * /opt/backup_files.sh" | crontab -
```

## Step 9: Deployment

### Manual Deployment

```bash
# Build and deploy
docker-compose -f docker-compose.production.yml build
docker-compose -f docker-compose.production.yml up -d

# Check logs
docker-compose -f docker-compose.production.yml logs -f
```

### CI/CD Deployment (GitHub Actions)

Create `.github/workflows/deploy-production.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest --cov=app

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: success()
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      
      - name: Set up SSH
        uses: webfactory/ssh-agent@v0.5.3
        with:
          ssh-private-key: ${{ secrets.PRODUCTION_SSH_KEY }}
      
      - name: Deploy to production
        run: |
          ssh -o StrictHostKeyChecking=no ${{ secrets.PRODUCTION_SSH_USER }}@${{ secrets.PRODUCTION_SSH_HOST }} << 'EOF'
            cd /opt/smartrent
            git pull
            docker-compose -f docker-compose.production.yml down
            docker-compose -f docker-compose.production.yml up -d --build
          EOF
```

## Step 10: Post-Deployment Verification

1. **Health Check**
   ```bash
   curl -i https://smartrent.com/health
   ```

2. **API Verification**
   ```bash
   curl -i https://smartrent.com/api/docs
   ```

3. **Monitor Logs**
   ```bash
   docker-compose -f docker-compose.production.yml logs -f
   ```

4. **Check Metrics in Grafana**
   - Review API response times
   - Monitor error rates
   - Check system resources

## Disaster Recovery Plan

1. **Database Failure**
   - Restore from latest backup
   - If using MongoDB Atlas, failover to a secondary node

2. **Server Failure**
   - If using cloud infrastructure, trigger auto-scaling or instance replacement
   - If using dedicated servers, restore from backup to new hardware

3. **Application Rollback**
   ```bash
   # Roll back to previous version
   git checkout <previous-commit>
   docker-compose -f docker-compose.production.yml down
   docker-compose -f docker-compose.production.yml up -d --build
   ```

## Security Considerations

1. **Firewall Configuration**
   - Only allow necessary ports (80, 443)
   - Restrict SSH access to trusted IP addresses

2. **Regular Updates**
   ```bash
   # Update server packages
   sudo apt update
   sudo apt upgrade -y
   
   # Update Docker images
   docker-compose -f docker-compose.production.yml pull
   docker-compose -f docker-compose.production.yml up -d
   ```

3. **Security Monitoring**
   - Set up intrusion detection
   - Configure log monitoring for suspicious activities
   - Implement rate limiting to prevent DoS attacks 