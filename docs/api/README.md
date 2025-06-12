# SmartRent API Documentation

## Overview

The SmartRent API provides a comprehensive set of endpoints for managing properties, users, and rental agreements. This documentation covers all available endpoints, authentication methods, and response formats.

## Authentication

### JWT Authentication
All API endpoints require JWT authentication unless otherwise specified.

```http
Authorization: Bearer <token>
```

### Token Types
- Access Token: Short-lived token for API access
- Refresh Token: Long-lived token for obtaining new access tokens

### Obtaining Tokens
1. Login endpoint: `/api/auth/login`
2. Refresh endpoint: `/api/auth/refresh`
3. Wallet authentication: `/api/auth/wallet`

## Rate Limiting

### Limits
- 100 requests per minute per IP
- 1000 requests per hour per user
- Burst limit: 20 requests per 10 seconds

### Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1617123456
```

## Error Handling

### Error Response Format
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": {
            "field": "Additional error details"
        }
    }
}
```

### Common Error Codes
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## Endpoints

### Authentication

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

Response:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "expires_in": 3600
}
```

### Properties

#### List Properties
```http
GET /api/properties
```

Query Parameters:
- `type`: Property type filter
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter
- `location`: Location filter
- `page`: Page number
- `limit`: Items per page

Response:
```json
{
    "items": [
        {
            "id": "property_123",
            "title": "Luxury Apartment",
            "description": "Beautiful view of the city",
            "price": 1500,
            "location": "New York",
            "type": "apartment",
            "status": "available"
        }
    ],
    "total": 100,
    "page": 1,
    "limit": 10
}
```

#### Create Property
```http
POST /api/properties
Authorization: Bearer <token>
Content-Type: application/json

{
    "title": "Luxury Apartment",
    "description": "Beautiful view of the city",
    "price": 1500,
    "location": "New York",
    "type": "apartment",
    "features": ["pool", "gym", "parking"]
}
```

Response:
```json
{
    "id": "property_123",
    "title": "Luxury Apartment",
    "description": "Beautiful view of the city",
    "price": 1500,
    "location": "New York",
    "type": "apartment",
    "status": "available",
    "created_at": "2025-04-07T10:20:00Z"
}
```

### Users

#### Get User Profile
```http
GET /api/users/me
Authorization: Bearer <token>
```

Response:
```json
{
    "id": "user_123",
    "email": "user@example.com",
    "role": "tenant",
    "wallet_address": "0x1234...",
    "created_at": "2025-01-01T00:00:00Z"
}
```

## WebSocket API

### Connection
```javascript
const ws = new WebSocket('wss://api.smartrent.com/ws');

ws.onopen = () => {
    console.log('Connected to WebSocket');
};

ws.onmessage = (event) => {
    console.log('Received:', event.data);
};
```

### Events

#### Property Updates
```json
{
    "event": "property_update",
    "data": {
        "id": "property_123",
        "status": "rented",
        "updated_at": "2025-04-07T10:20:00Z"
    }
}
```

#### Transaction Updates
```json
{
    "event": "transaction_update",
    "data": {
        "id": "tx_123",
        "status": "confirmed",
        "block_hash": "0x1234...",
        "updated_at": "2025-04-07T10:20:00Z"
    }
}
```

## SDKs and Libraries

### Python SDK
```python
from smartrent import SmartRentClient

client = SmartRentClient(api_key='your_api_key')
properties = client.properties.list()
```

### JavaScript SDK
```javascript
import { SmartRent } from '@smartrent/sdk';

const client = new SmartRent({
    apiKey: 'your_api_key'
});

const properties = await client.properties.list();
```

## Best Practices

### Authentication
- Always use HTTPS
- Store tokens securely
- Implement token refresh logic
- Handle token expiration gracefully

### Error Handling
- Implement exponential backoff
- Log errors appropriately
- Provide meaningful error messages
- Handle rate limiting

### Performance
- Use pagination for large datasets
- Implement caching where appropriate
- Minimize request payload size
- Use compression for large responses

## Support

For API support, please contact:
- Email: support@smartrent.com
- Documentation: https://docs.smartrent.com
- Status Page: https://status.smartrent.com 