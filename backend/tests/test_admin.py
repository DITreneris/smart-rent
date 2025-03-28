import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from ..app.models import User, Property, Contract, UserStatus, PropertyStatus


@pytest.fixture
def pending_user(db):
    """Create a pending user for testing approval."""
    user = User(
        email="pending@example.com",
        hashed_password="$2b$12$HxjEkIgt9.Y/xaRYbVw8XOTf1BNIYHzHLVO55zWKgcQZ6yvKpUzNW",  # password = 'Password123'
        full_name="Pending User",
        role="tenant",
        status=UserStatus.PENDING,
        created_at=datetime.now()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def pending_property(db, landlord_user):
    """Create a pending property for testing approval."""
    property_item = Property(
        title="Pending Property",
        description="A property waiting for approval",
        address="789 Pending St, Pending City, PC 24680",
        price=175000,  # $1,750.00
        owner_id=landlord_user.id,
        status=PropertyStatus.PENDING,
        images=["http://example.com/pending1.jpg"],
        features={"bedrooms": 3, "bathrooms": 2, "sqft": 1800},
        created_at=datetime.now()
    )
    db.add(property_item)
    db.commit()
    db.refresh(property_item)
    return property_item


def test_access_admin_endpoints_as_non_admin(client, tenant_token):
    """Test accessing admin endpoints as a non-admin user."""
    response = client.get(
        "/api/v1/admin/pending-users",
        headers={"Authorization": f"Bearer {tenant_token}"}
    )
    assert response.status_code == 403
    assert "Admin access required" in response.json()["detail"]


def test_get_pending_users(client, admin_token, pending_user):
    """Test getting pending users as an admin."""
    response = client.get(
        "/api/v1/admin/pending-users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # Find our pending user in the list
    found = False
    for user in data:
        if user["email"] == pending_user.email:
            found = True
            assert user["status"] == "pending"
    assert found, "Pending user not found in the list"


def test_approve_user(client, admin_token, pending_user):
    """Test approving a user as an admin."""
    response = client.post(
        f"/api/v1/admin/approve-user/{pending_user.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"approved": True, "notes": "User approved after verification"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pending_user.id
    assert data["status"] == "approved"


def test_reject_user(client, admin_token, pending_user):
    """Test rejecting a user as an admin."""
    response = client.post(
        f"/api/v1/admin/approve-user/{pending_user.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"approved": False, "notes": "Insufficient information provided"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pending_user.id
    assert data["status"] == "rejected"


def test_get_pending_properties(client, admin_token, pending_property):
    """Test getting pending properties as an admin."""
    response = client.get(
        "/api/v1/admin/pending-properties",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # Find our pending property in the list
    found = False
    for prop in data:
        if prop["id"] == pending_property.id:
            found = True
            assert prop["status"] == "pending"
    assert found, "Pending property not found in the list"


def test_approve_property(client, admin_token, pending_property):
    """Test approving a property as an admin."""
    response = client.post(
        f"/api/v1/admin/approve-property/{pending_property.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"approved": True, "notes": "Property meets standards"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pending_property.id
    assert data["status"] == "approved"


def test_reject_property(client, admin_token, pending_property):
    """Test rejecting a property as an admin."""
    response = client.post(
        f"/api/v1/admin/approve-property/{pending_property.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"approved": False, "notes": "Listing incomplete"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pending_property.id
    assert data["status"] == "rejected"


def test_get_dashboard_stats(client, admin_token, pending_user, pending_property):
    """Test getting dashboard statistics as an admin."""
    response = client.get(
        "/api/v1/admin/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "tenant_count" in data
    assert "landlord_count" in data
    assert "pending_approvals" in data
    assert "property_stats" in data
    assert "contract_stats" in data
    
    # Verify that our pending user and property are counted
    assert data["pending_approvals"]["users"] >= 1
    assert data["pending_approvals"]["properties"] >= 1 