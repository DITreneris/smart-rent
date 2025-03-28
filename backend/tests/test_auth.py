import pytest
from fastapi.testclient import TestClient
import json

from ..app.models import UserStatus


def test_login_valid_credentials(client):
    """Test login with valid credentials."""
    # Send a login request with valid credentials
    response = client.post(
        "/api/v1/login",
        data={"username": "tenant@example.com", "password": "Password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    # Send a login request with invalid credentials
    response = client.post(
        "/api/v1/login",
        data={"username": "tenant@example.com", "password": "WrongPassword"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()


def test_register_tenant(client, db):
    """Test tenant registration."""
    # Send a tenant registration request
    response = client.post(
        "/api/v1/register/tenant",
        json={
            "email": "new_tenant@example.com",
            "password": "Password123",
            "full_name": "New Tenant User"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "new_tenant@example.com"
    assert data["full_name"] == "New Tenant User"
    assert data["role"] == "tenant"
    assert data["status"] == "pending"


def test_register_landlord(client, db):
    """Test landlord registration."""
    # Send a landlord registration request
    response = client.post(
        "/api/v1/register/landlord",
        json={
            "email": "new_landlord@example.com",
            "password": "Password123",
            "full_name": "New Landlord User"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "new_landlord@example.com"
    assert data["full_name"] == "New Landlord User"
    assert data["role"] == "landlord"
    assert data["status"] == "pending"


def test_register_existing_email(client, tenant_user):
    """Test registration with an existing email."""
    # Try to register with an email that is already in use
    response = client.post(
        "/api/v1/register/tenant",
        json={
            "email": "tenant@example.com",  # Already exists
            "password": "Password123",
            "full_name": "Duplicate User"
        },
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_get_current_user(client, tenant_token):
    """Test getting the current user's data."""
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {tenant_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "tenant@example.com"
    assert data["full_name"] == "Test Tenant"
    assert data["role"] == "tenant"


def test_update_user(client, tenant_token, db):
    """Test updating user profile."""
    response = client.put(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {tenant_token}"},
        json={
            "full_name": "Updated Tenant Name",
            "wallet_address": "0x1234567890abcdef1234567890abcdef12345678"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Tenant Name"
    assert data["wallet_address"] == "0x1234567890abcdef1234567890abcdef12345678"


def test_unauthorized_access(client):
    """Test access without authentication."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert "detail" in response.json() 