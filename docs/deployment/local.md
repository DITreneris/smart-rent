# Local Deployment

This guide covers how to set up and run SmartRent locally for development purposes.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.9+
- MongoDB 4.4+
- Node.js 16+
- Git
- (Optional) Redis for caching

## Step 1: Clone the Repository

```bash
git clone https://github.com/DITreneris/smart-rent.git
cd smart-rent
```

## Step 2: Set Up Backend

### Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file to set up your local configuration:

```env
# Basic settings
DEBUG=True
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here

# Database settings
MONGO_CONNECTION_STRING=mongodb://localhost:27017/
MONGO_DB_NAME=smartrent_dev

# Web3 settings (can use Ganache for local development)
WEB3_PROVIDER_URL=http://localhost:8545
CONTRACT_ADDRESS=0x123...  # Your contract address

# Admin user
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=securepassword
ADMIN_FULL_NAME=Admin User
```

### Start MongoDB

```bash
# If MongoDB is not running as a service:
mongod --dbpath /path/to/data
```

## Step 3: Run the Backend

```bash
# From the project root
uvicorn app.main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

API documentation will be available at:
- Swagger UI: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- ReDoc: [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)

## Step 4: Set Up Frontend (If Applicable)

If the project includes a frontend application:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will typically be available at [http://localhost:3000](http://localhost:3000).

## Step 5: Initialize Database (Optional)

To populate the database with sample data:

```bash
# From the project root with virtual environment activated
python scripts/seed_database.py
```

This will create sample users, properties, and other data for testing.

## Development Tools

### Running Tests

```bash
# From the project root with virtual environment activated
pytest
```

For specific test files:

```bash
pytest tests/test_auth.py
```

With coverage:

```bash
pytest --cov=app
```

### Code Formatting

Format Python code:

```bash
black app tests
```

Sort imports:

```bash
isort app tests
```

### Linting

Lint Python code:

```bash
flake8 app tests
```

## Troubleshooting

### MongoDB Connection Issues

If you encounter MongoDB connection issues:

1. Ensure MongoDB is running
2. Verify the connection string in your `.env` file
3. Check that the database name is correct
4. Ensure the MongoDB port is not blocked by a firewall

### Import Errors

If you encounter import errors:

1. Make sure your virtual environment is activated
2. Verify all dependencies are installed
3. Check if Python path is set correctly

### API Errors

For API-related errors:

1. Check the console output for detailed error messages
2. Verify environment variables are set correctly
3. Ensure MongoDB is running and accessible

## Next Steps

After setting up your local development environment, you might want to:

1. Explore the API using the Swagger documentation
2. Set up a local blockchain environment using Ganache for testing
3. Review the [developer documentation](../developer/README.md) for code architecture
4. Check out [contributing guidelines](../contributing/README.md) to understand how to contribute

## Getting Help

If you encounter issues with the local setup:

1. Check the error logs
2. Search for similar issues in the GitHub repository
3. Ask for help in the community channels 