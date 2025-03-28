import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from ..app.models import Contract, ContractStatus, Property, PropertyStatus


@pytest.fixture
def test_property(db, landlord_user):
    """Create a test property for contract testing."""
    property_item = Property(
        title="Rental Property",
        description="A property available for rent",
        address="456 Rental St, Rental City, RC 67890",
        price=200000,  # $2,000.00
        owner_id=landlord_user.id,
        status=PropertyStatus.APPROVED,
        images=["http://example.com/rental1.jpg"],
        features={"bedrooms": 2, "bathrooms": 1, "sqft": 1200},
        created_at=datetime.now()
    )
    db.add(property_item)
    db.commit()
    db.refresh(property_item)
    return property_item


@pytest.fixture
def test_contract(db, tenant_user, landlord_user, test_property):
    """Create a test contract for testing."""
    contract = Contract(
        property_id=test_property.id,
        tenant_id=tenant_user.id,
        landlord_id=landlord_user.id,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=365),
        monthly_rent=test_property.price,
        security_deposit=test_property.price * 2,
        status=ContractStatus.PENDING,
        created_at=datetime.now()
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


def test_create_contract(client, tenant_token, test_property):
    """Test creating a new rental contract."""
    start_date = datetime.now() + timedelta(days=30)
    end_date = start_date + timedelta(days=365)
    
    response = client.post(
        "/api/v1/contracts",
        headers={"Authorization": f"Bearer {tenant_token}"},
        json={
            "property_id": test_property.id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "monthly_rent": test_property.price,
            "security_deposit": test_property.price * 2
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["property_id"] == test_property.id
    assert data["status"] == "pending"


def test_create_contract_as_landlord(client, landlord_token, test_property):
    """Test creating a contract as a landlord (should fail)."""
    start_date = datetime.now() + timedelta(days=30)
    end_date = start_date + timedelta(days=365)
    
    response = client.post(
        "/api/v1/contracts",
        headers={"Authorization": f"Bearer {landlord_token}"},
        json={
            "property_id": test_property.id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "monthly_rent": test_property.price,
            "security_deposit": test_property.price * 2
        }
    )
    assert response.status_code == 403
    assert "Only tenants can request rental contracts" in response.json()["detail"]


def test_list_contracts_as_tenant(client, tenant_token, test_contract):
    """Test listing contracts as a tenant."""
    response = client.get(
        "/api/v1/contracts",
        headers={"Authorization": f"Bearer {tenant_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # Tenant should only see their own contracts
    for contract in data:
        assert "property_id" in contract
        assert "start_date" in contract
        assert "end_date" in contract
        assert "status" in contract


def test_list_contracts_as_landlord(client, landlord_token, test_contract):
    """Test listing contracts as a landlord."""
    response = client.get(
        "/api/v1/contracts",
        headers={"Authorization": f"Bearer {landlord_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    # Landlord should only see contracts related to their properties
    for contract in data:
        assert "property_id" in contract
        assert "tenant_id" in contract
        assert "start_date" in contract


def test_get_contract_details(client, tenant_token, test_contract):
    """Test getting contract details."""
    response = client.get(
        f"/api/v1/contracts/{test_contract.id}",
        headers={"Authorization": f"Bearer {tenant_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_contract.id
    assert data["property_id"] == test_contract.property_id
    assert data["status"] == "pending"


def test_confirm_contract(client, landlord_token, test_contract):
    """Test confirming a contract by the landlord."""
    response = client.put(
        f"/api/v1/contracts/{test_contract.id}/confirm",
        headers={"Authorization": f"Bearer {landlord_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    
    # Check that property status is updated
    response = client.get(
        f"/api/v1/properties/{test_contract.property_id}",
        headers={"Authorization": f"Bearer {landlord_token}"}
    )
    assert response.json()["status"] == "rented"


def test_confirm_contract_as_tenant(client, tenant_token, test_contract):
    """Test confirming a contract as a tenant (should fail)."""
    response = client.put(
        f"/api/v1/contracts/{test_contract.id}/confirm",
        headers={"Authorization": f"Bearer {tenant_token}"}
    )
    assert response.status_code == 403
    assert "Only the landlord can confirm this contract" in response.json()["detail"]


def test_cancel_contract_as_tenant(client, tenant_token, test_contract):
    """Test canceling a contract as a tenant."""
    response = client.put(
        f"/api/v1/contracts/{test_contract.id}/cancel",
        headers={"Authorization": f"Bearer {tenant_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "cancelled"
    
    # Check that property status is updated
    response = client.get(
        f"/api/v1/properties/{test_contract.property_id}",
        headers={"Authorization": f"Bearer {tenant_token}"}
    )
    assert response.json()["status"] == "approved"


def test_complete_contract(client, landlord_token, test_contract, db):
    """Test completing a contract by the landlord."""
    # First make the contract active
    test_contract.status = ContractStatus.ACTIVE
    db.commit()
    
    response = client.put(
        f"/api/v1/contracts/{test_contract.id}/complete",
        headers={"Authorization": f"Bearer {landlord_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    
    # Check that property status is updated
    response = client.get(
        f"/api/v1/properties/{test_contract.property_id}",
        headers={"Authorization": f"Bearer {landlord_token}"}
    )
    assert response.json()["status"] == "approved" 