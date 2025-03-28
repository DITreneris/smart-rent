"""End-to-end integration tests for the Smart Rent Platform API."""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import json

from .utils import assert_keys_in_dict
from ..app.models import UserStatus, PropertyStatus, ContractStatus


@pytest.mark.integration
def test_end_to_end_rental_flow(client, db):
    """Test the full rental flow from registration to contract completion."""
    # 1. Register a tenant and landlord
    tenant_data = {
        "email": "e2e_tenant@example.com",
        "password": "SecurePassword123",
        "full_name": "E2E Tenant"
    }
    
    landlord_data = {
        "email": "e2e_landlord@example.com",
        "password": "SecurePassword123",
        "full_name": "E2E Landlord"
    }
    
    tenant_response = client.post("/api/v1/register/tenant", json=tenant_data)
    assert tenant_response.status_code == 200
    tenant_id = tenant_response.json()["id"]
    
    landlord_response = client.post("/api/v1/register/landlord", json=landlord_data)
    assert landlord_response.status_code == 200
    landlord_id = landlord_response.json()["id"]
    
    # 2. Admin login
    admin_login = client.post(
        "/api/v1/login",
        data={"username": "admin@example.com", "password": "Password123"},
    )
    assert admin_login.status_code == 200
    admin_token = admin_login.json()["access_token"]
    
    # 3. Admin approves both users
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    approve_tenant = client.post(
        f"/api/v1/admin/approve-user/{tenant_id}",
        headers=admin_headers,
        json={"approved": True, "notes": "E2E test tenant approval"}
    )
    assert approve_tenant.status_code == 200
    assert approve_tenant.json()["status"] == "approved"
    
    approve_landlord = client.post(
        f"/api/v1/admin/approve-user/{landlord_id}",
        headers=admin_headers,
        json={"approved": True, "notes": "E2E test landlord approval"}
    )
    assert approve_landlord.status_code == 200
    assert approve_landlord.json()["status"] == "approved"
    
    # 4. Landlord login and create property
    landlord_login = client.post(
        "/api/v1/login",
        data={"username": "e2e_landlord@example.com", "password": "SecurePassword123"},
    )
    assert landlord_login.status_code == 200
    landlord_token = landlord_login.json()["access_token"]
    landlord_headers = {"Authorization": f"Bearer {landlord_token}"}
    
    property_data = {
        "title": "E2E Test Property",
        "description": "A property for end-to-end testing",
        "address": "123 E2E Street, Test City, TC 12345",
        "price": 200000,  # $2,000.00
        "images": ["http://example.com/e2e_image1.jpg"],
        "features": {"bedrooms": 2, "bathrooms": 2, "sqft": 1200}
    }
    
    property_response = client.post(
        "/api/v1/properties",
        headers=landlord_headers,
        json=property_data
    )
    assert property_response.status_code == 200
    property_id = property_response.json()["id"]
    
    # 5. Admin approves property
    approve_property = client.post(
        f"/api/v1/admin/approve-property/{property_id}",
        headers=admin_headers,
        json={"approved": True, "notes": "E2E test property approval"}
    )
    assert approve_property.status_code == 200
    assert approve_property.json()["status"] == "approved"
    
    # 6. Tenant login and view property
    tenant_login = client.post(
        "/api/v1/login",
        data={"username": "e2e_tenant@example.com", "password": "SecurePassword123"},
    )
    assert tenant_login.status_code == 200
    tenant_token = tenant_login.json()["access_token"]
    tenant_headers = {"Authorization": f"Bearer {tenant_token}"}
    
    property_details = client.get(
        f"/api/v1/properties/{property_id}",
        headers=tenant_headers
    )
    assert property_details.status_code == 200
    assert property_details.json()["id"] == property_id
    
    # 7. Tenant creates a contract request
    start_date = (datetime.now() + timedelta(days=30)).isoformat()
    end_date = (datetime.now() + timedelta(days=395)).isoformat()
    
    contract_data = {
        "property_id": property_id,
        "start_date": start_date,
        "end_date": end_date,
        "monthly_rent": 200000,
        "security_deposit": 400000
    }
    
    contract_response = client.post(
        "/api/v1/contracts",
        headers=tenant_headers,
        json=contract_data
    )
    assert contract_response.status_code == 200
    contract_id = contract_response.json()["id"]
    assert contract_response.json()["status"] == "pending"
    
    # 8. Landlord confirms the contract
    confirm_contract = client.put(
        f"/api/v1/contracts/{contract_id}/confirm",
        headers=landlord_headers
    )
    assert confirm_contract.status_code == 200
    assert confirm_contract.json()["status"] == "active"
    
    # 9. Check that property status is now rented
    property_details = client.get(
        f"/api/v1/properties/{property_id}",
        headers=landlord_headers
    )
    assert property_details.status_code == 200
    assert property_details.json()["status"] == "rented"
    
    # 10. Landlord completes the contract after the rental period
    complete_contract = client.put(
        f"/api/v1/contracts/{contract_id}/complete",
        headers=landlord_headers
    )
    assert complete_contract.status_code == 200
    assert complete_contract.json()["status"] == "completed"
    
    # 11. Check that property status is back to approved
    property_details = client.get(
        f"/api/v1/properties/{property_id}",
        headers=landlord_headers
    )
    assert property_details.status_code == 200
    assert property_details.json()["status"] == "approved"
    
    # 12. Check dashboard stats as admin
    dashboard = client.get(
        "/api/v1/admin/dashboard",
        headers=admin_headers
    )
    assert dashboard.status_code == 200
    stats = dashboard.json()
    
    # Verify counters have been updated
    assert stats["tenant_count"] >= 1
    assert stats["landlord_count"] >= 1
    assert stats["property_stats"]["total"] >= 1
    assert stats["contract_stats"]["completed"] >= 1 