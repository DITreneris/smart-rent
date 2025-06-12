# Developer Setup Guide

## Environment Setup

### 1. Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. MongoDB Setup
```bash
# Install MongoDB
# Windows: Download and install MongoDB Community Server
# Ubuntu: sudo apt-get install mongodb
# MacOS: brew install mongodb-community

# Start MongoDB
mongod --dbpath /path/to/data
```

### 3. Environment Variables
Create `.env` file with:
```env
MONGODB_URL=mongodb://localhost:27017
JWT_SECRET=your-secret-key
DEBUG=True
```

## Running the Application

### Development Server
```bash
uvicorn app.main:app --reload
```

### Access API Documentation
- OpenAPI docs: http://localhost:8000/docs
- ReDoc docs: http://localhost:8000/redoc

## Common Issues

### MongoDB Connection
- Ensure MongoDB is running
- Check connection string in .env
- Verify MongoDB port (default: 27017)

### Python Dependencies
- Update pip: `python -m pip install --upgrade pip`
- Clear pip cache: `pip cache purge`
- Reinstall requirements: `pip install -r requirements.txt`

### JWT Authentication
- Verify JWT_SECRET in .env
- Check token expiration
- Ensure proper role assignment

## Development Workflow

### 1. Code Changes
- Make changes in feature branch
- Run tests: `pytest`
- Check formatting: `black .`
- Verify imports: `isort .`

### 2. Testing
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app
```

### 3. API Testing
```bash
# Using curl
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@tenant.com","password":"demo123"}'

# Using Python requests
import requests
response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={"email": "demo@tenant.com", "password": "demo123"}
)
print(response.json())
```

## Support
For development issues:
- Check error logs
- Review API documentation
- Contact: dev-support@smartrent.com 