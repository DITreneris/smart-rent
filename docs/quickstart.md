# SmartRent Demo - Quick Start Guide

## Prerequisites
- Python 3.9+
- MongoDB 4.4+
- Git

## Installation

1. **Clone Repository**
```bash
git clone https://github.com/DITreneris/smart-rent.git
cd smart-rent
```

2. **Set Up Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start MongoDB**
```bash
mongod --dbpath /path/to/data
```

5. **Run Application**
```bash
uvicorn app.main:app --reload
```

## Demo Features

### Available Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/properties` - List properties
- `POST /api/properties` - Create property
- `GET /api/properties/{id}` - Get property details

### Test Accounts
- Landlord: demo@landlord.com / demo123
- Tenant: demo@tenant.com / demo123
- Admin: demo@admin.com / demo123

## Next Steps
1. Create your first property listing
2. Test the authentication flow
3. Explore the API endpoints
4. Check the demo limitations

## Support
For demo-related issues, contact: support@smartrent.com 