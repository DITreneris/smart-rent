# Smart Rent Platform API Documentation

## Overview

This document provides detailed information about the Smart Rent Platform API endpoints. The API is built using FastAPI and follows RESTful principles.

Base URL: `http://localhost:8000/api/v1`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Endpoints

#### Register a new user

```
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "tenant"  // Options: "tenant", "landlord", "admin"
}
```

**Response:**
```json
{
  "id": "user_id",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "tenant",
  "created_at": "2023-06-15T10:00:00"
}
```

#### Login

```
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "tenant"
  }
}
```

#### Get current user

```
GET /auth/me
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": "user_id",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "tenant",
  "created_at": "2023-06-15T10:00:00"
}
```

## Properties

### Endpoints

#### Get all properties

```
GET /properties
```

**Query Parameters:**
- `location` (optional): Filter by location
- `min_price` (optional): Minimum price
- `max_price` (optional): Maximum price
- `available` (optional): Filter by availability (true/false)
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)

**Response:**
```json
{
  "items": [
    {
      "id": "property_id",
      "title": "Modern Apartment",
      "description": "Beautiful modern apartment in the city center",
      "location": "New York",
      "price": 1500,
      "landlord_id": "landlord_id",
      "available": true,
      "images": ["url1", "url2"],
      "features": ["wifi", "parking", "gym"],
      "created_at": "2023-06-15T10:00:00"
    }
  ],
  "total": 100,
  "page": 1,
  "limit": 10
}
```

#### Get property by ID

```
GET /properties/{property_id}
```

**Response:**
```json
{
  "id": "property_id",
  "title": "Modern Apartment",
  "description": "Beautiful modern apartment in the city center",
  "location": "New York",
  "price": 1500,
  "landlord_id": "landlord_id",
  "landlord": {
    "id": "landlord_id",
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com"
  },
  "available": true,
  "images": ["url1", "url2"],
  "features": ["wifi", "parking", "gym"],
  "created_at": "2023-06-15T10:00:00"
}
```

#### Create a new property

```
POST /properties
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "Modern Apartment",
  "description": "Beautiful modern apartment in the city center",
  "location": "New York",
  "price": 1500,
  "images": ["url1", "url2"],
  "features": ["wifi", "parking", "gym"]
}
```

**Response:**
```json
{
  "id": "property_id",
  "title": "Modern Apartment",
  "description": "Beautiful modern apartment in the city center",
  "location": "New York",
  "price": 1500,
  "landlord_id": "landlord_id",
  "available": true,
  "images": ["url1", "url2"],
  "features": ["wifi", "parking", "gym"],
  "created_at": "2023-06-15T10:00:00"
}
```

#### Update a property

```
PUT /properties/{property_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "Updated Apartment",
  "description": "Updated description",
  "price": 1600,
  "available": false
}
```

**Response:**
```json
{
  "id": "property_id",
  "title": "Updated Apartment",
  "description": "Updated description",
  "location": "New York",
  "price": 1600,
  "landlord_id": "landlord_id",
  "available": false,
  "images": ["url1", "url2"],
  "features": ["wifi", "parking", "gym"],
  "created_at": "2023-06-15T10:00:00",
  "updated_at": "2023-06-16T10:00:00"
}
```

#### Delete a property

```
DELETE /properties/{property_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "message": "Property deleted successfully"
}
```

## Contracts

### Endpoints

#### Get all contracts

```
GET /contracts
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `status` (optional): Filter by status (pending, active, completed, canceled)
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)

**Response:**
```json
{
  "items": [
    {
      "id": "contract_id",
      "property_id": "property_id",
      "tenant_id": "tenant_id",
      "landlord_id": "landlord_id",
      "start_date": "2023-07-01",
      "end_date": "2024-06-30",
      "monthly_rent": 1500,
      "security_deposit": 3000,
      "status": "active",
      "blockchain_id": "0x1234...",
      "created_at": "2023-06-15T10:00:00"
    }
  ],
  "total": 5,
  "page": 1,
  "limit": 10
}
```

#### Get contract by ID

```
GET /contracts/{contract_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": "contract_id",
  "property_id": "property_id",
  "property": {
    "id": "property_id",
    "title": "Modern Apartment",
    "location": "New York",
    "price": 1500
  },
  "tenant_id": "tenant_id",
  "tenant": {
    "id": "tenant_id",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
  },
  "landlord_id": "landlord_id",
  "landlord": {
    "id": "landlord_id",
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com"
  },
  "start_date": "2023-07-01",
  "end_date": "2024-06-30",
  "monthly_rent": 1500,
  "security_deposit": 3000,
  "status": "active",
  "blockchain_id": "0x1234...",
  "payment_history": [
    {
      "id": "payment_id",
      "amount": 1500,
      "date": "2023-07-01T10:00:00",
      "transaction_hash": "0xabcd..."
    }
  ],
  "created_at": "2023-06-15T10:00:00"
}
```

#### Create a new contract

```
POST /contracts
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "property_id": "property_id",
  "tenant_id": "tenant_id",
  "start_date": "2023-07-01",
  "end_date": "2024-06-30",
  "monthly_rent": 1500,
  "security_deposit": 3000
}
```

**Response:**
```json
{
  "id": "contract_id",
  "property_id": "property_id",
  "tenant_id": "tenant_id",
  "landlord_id": "landlord_id",
  "start_date": "2023-07-01",
  "end_date": "2024-06-30",
  "monthly_rent": 1500,
  "security_deposit": 3000,
  "status": "pending",
  "blockchain_id": null,
  "created_at": "2023-06-15T10:00:00"
}
```

#### Update contract status

```
PATCH /contracts/{contract_id}/status
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "status": "active"
}
```

**Response:**
```json
{
  "id": "contract_id",
  "status": "active",
  "updated_at": "2023-06-16T10:00:00"
}
```

## Admin

### Endpoints

#### Get system stats

```
GET /admin/stats
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "users": {
    "total": 100,
    "landlords": 40,
    "tenants": 58,
    "admins": 2
  },
  "properties": {
    "total": 60,
    "available": 25,
    "rented": 35
  },
  "contracts": {
    "total": 35,
    "active": 30,
    "pending": 3,
    "completed": 2,
    "canceled": 0
  },
  "transactions": {
    "total": 120,
    "value": 180000
  }
}
```

#### Manage user roles

```
PUT /admin/users/{user_id}/role
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "user_type": "admin"
}
```

**Response:**
```json
{
  "id": "user_id",
  "email": "user@example.com",
  "user_type": "admin",
  "updated_at": "2023-06-16T10:00:00"
}
```

## Blockchain

### Endpoints

#### Check blockchain status

```
GET /blockchain/status
```

**Response:**
```json
{
  "network": "Sepolia Testnet",
  "block_number": 12345678,
  "gas_price": "20 Gwei",
  "connected": true
}
```

#### Create rental agreement on blockchain

```
POST /blockchain/agreements
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "property_id": "property123",
  "tenant_address": "0x1234...",
  "landlord_address": "0x5678...",
  "start_date": 1688169600,
  "end_date": 1719792000,
  "monthly_rent": "0.2",
  "security_deposit": "0.4"
}
```

**Response:**
```json
{
  "agreement_id": 1,
  "transaction_hash": "0xabcd...",
  "block_number": 12345678,
  "gas_used": 250000
}
```

#### Get blockchain agreement details

```
GET /blockchain/agreements/{id}
```

**Response:**
```json
{
  "agreement_id": 1,
  "property_id": "property123",
  "tenant": "0x1234...",
  "landlord": "0x5678...",
  "start_date": 1688169600,
  "end_date": 1719792000,
  "monthly_rent": "0.2",
  "security_deposit": "0.4",
  "last_payment_date": 1688169600,
  "status": "Active"
}
```

#### Get agreements for a tenant

```
GET /blockchain/tenant/{address}/agreements
```

**Response:**
```json
{
  "agreements": [1, 2, 3]
}
```

#### Get agreements for a landlord

```
GET /blockchain/landlord/{address}/agreements
```

**Response:**
```json
{
  "agreements": [1, 4, 5]
}
```

#### Verify wallet signature

```
POST /blockchain/verify-signature
```

**Request Body:**
```json
{
  "address": "0x1234...",
  "message": "Login to Smart Rent: 12345",
  "signature": "0xabc123..."
}
```

**Response:**
```json
{
  "valid": true,
  "address": "0x1234..."
}
```

#### Get wallet balance

```
GET /blockchain/balance/{address}
```

**Response:**
```json
{
  "address": "0x1234...",
  "balance": "1.5",
  "currency": "ETH"
}
```

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized

```json
{
  "detail": "Invalid authentication credentials"
}
```

### 403 Forbidden

```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found

```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error

```json
{
  "detail": "Validation error message"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Limits are as follows:

- Unauthenticated requests: 60 requests per minute
- Authenticated requests: 120 requests per minute

Exceeding these limits will result in a 429 Too Many Requests response.

## Pagination

Endpoints that return lists of items support pagination through the following query parameters:

- `page`: Page number (starts at 1)
- `limit`: Number of items per page

The response will include pagination metadata:

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 10
}
```

## Filtering

Many endpoints support filtering through query parameters. The available filters are documented for each endpoint.

## Sorting

Endpoints that return lists can be sorted using the `sort` query parameter, with an optional `order` parameter to specify the direction:

```
GET /properties?sort=price&order=desc
```

## API Versioning

The API uses URL versioning. The current version is v1, and it is accessed through the `/api/v1` prefix. 