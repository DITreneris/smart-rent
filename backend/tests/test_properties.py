import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from ..app.models import Property, PropertyStatus


@pytest.fixture
def test_property(db, landlord_user):
    """Create a test property for testing."""
    property_item = Property(
        title="Test Property",
        description="A test property for unit testing",
        address="123 Test St, Test City, TS 12345",
        price=150000,  # $1,500.00
        owner_id=landlord_user.id,
        status=PropertyStatus.APPROVED,
        images=["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
        features={"bedrooms": 3, "bathrooms": 2, "sqft": 1500},
        created_at=datetime.now()
    )
    db.add(property_item)
    db.commit()
    db.refresh(property_item)
    return property_item


def test_create_property(client, landlord_token):
    """Test creating a new property listing."""
    response = client.post(
        "/api/v1/properties",
        headers={"Authorization": f"Bearer {landlord_token}"},
        json={
            "title": "New Test Property",
            "description": "A brand new property listing",
            "address": "456 New St, New City, NS 67890",
            "price": 200000,  # $2,000.00
            "images": ["http://example.com/newimage1.jpg"],
            "features": {"bedrooms": 2, "bathrooms": 1, "sqft": 1000}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Test Property"
    assert data["price"] == 200000
    assert data["status"] == "pending"  # New properties start as pending


def test_create_property_as_tenant(client, tenant_token):
    """Test creating a property as a tenant (should fail)."""
    response = client.post(
        "/api/v1/properties",
        headers={"Authorization": f"Bearer {tenant_token}"},
        json={
            "title": "Tenant Property",
            "description": "A property created by a tenant",
            "address": "789 Tenant St, Tenant City, TC 13579",
            "price": 100000,
            "images": [],
            "features": {}
        }
    )
    assert response.status_code == 403
    assert "Only landlords can create property listings" in response.json()["detail"]


def test_list_properties_as_tenant(client, tenant_token, test_property):
    """Test listing properties as a tenant."""
    response = client.get(
        "/api/v1/properties",
        headers={"Authorization": f"Bearer {tenant_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # Tenants should only see approved properties
    for property_item in data:
        assert property_item["status"] == "approved"


def test_list_properties_as_landlord(client, landlord_token, test_property):
    """Test listing properties as a landlord."""
    response = client.get(
        "/api/v1/properties",
        headers={"Authorization": f"Bearer {landlord_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # Landlords should only see their own properties
    for property_item in data:
        assert "title" in property_item
        assert "price" in property_item


def test_get_property_details(client, tenant_token, test_property):
    """Test getting property details."""
    response = client.get(
        f"/api/v1/properties/{test_property.id}",
        headers={"Authorization": f"Bearer {tenant_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_property.id
    assert data["title"] == test_property.title
    assert data["price"] == test_property.price


def test_update_property(client, landlord_token, test_property):
    """Test updating a property."""
    response = client.put(
        f"/api/v1/properties/{test_property.id}",
        headers={"Authorization": f"Bearer {landlord_token}"},
        json={
            "title": "Updated Property Title",
            "price": 180000  # $1,800.00
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Property Title"
    assert data["price"] == 180000
    assert data["status"] == "pending"  # Updated properties go back to pending


def test_update_property_unauthorized(client, tenant_token, test_property):
    """Test updating a property without proper authorization."""
    response = client.put(
        f"/api/v1/properties/{test_property.id}",
        headers={"Authorization": f"Bearer {tenant_token}"},
        json={
            "title": "Tenant Updated Title",
            "price": 120000
        }
    )
    assert response.status_code == 403


def test_delete_property(client, landlord_token, test_property):
    """Test deleting a property."""
    response = client.delete(
        f"/api/v1/properties/{test_property.id}",
        headers={"Authorization": f"Bearer {landlord_token}"}
    )
    assert response.status_code == 204
    
    # Verify property is deleted
    response = client.get(
        f"/api/v1/properties/{test_property.id}",
        headers={"Authorization": f"Bearer {landlord_token}"}
    )
    assert response.status_code == 404


def test_delete_property_unauthorized(client, tenant_token, test_property):
    """Test deleting a property without proper authorization."""
    response = client.delete(
        f"/api/v1/properties/{test_property.id}",
        headers={"Authorization": f"Bearer {tenant_token}"}
    )
    assert response.status_code == 403 