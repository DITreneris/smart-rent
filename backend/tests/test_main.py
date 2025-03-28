import pytest
from fastapi.testclient import TestClient

from ..main import app


def test_root_endpoint():
    """Test the root endpoint of the API."""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Welcome to Smart Rent Platform API" in data["message"]
        assert "version" in data
        assert "status" in data


def test_cors_headers():
    """Test CORS headers are properly set."""
    with TestClient(app) as client:
        response = client.options(
            "/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
        assert "access-control-allow-methods" in response.headers
        assert "GET" in response.headers["access-control-allow-methods"]


def test_validation_error_handling():
    """Test validation error handling."""
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/register/tenant",
            json={
                "email": "not-an-email",  # Invalid email
                "password": "pass",  # Too short
                "full_name": ""  # Empty
            },
        )
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data 