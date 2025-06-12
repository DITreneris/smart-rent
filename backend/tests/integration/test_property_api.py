"""
Integration tests for Property API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestPropertyAPI:
    """Test cases for the Property API endpoints."""

    @pytest.mark.asyncio
    async def test_create_property(self, test_client, test_property_data, test_user, empty_test_database):
        """Test creating a new property."""
        # Add the owner_id to the property data
        property_data = {**test_property_data, "owner_id": test_user["_id"]}
        
        response = test_client.post(
            "/api/properties", 
            json=property_data,
            headers={"Authorization": f"Bearer {test_user.get('access_token', 'fake_token')}"}
        )
        
        assert response.status_code == 201
        property_obj = response.json()
        assert property_obj["title"] == property_data["title"]
        assert property_obj["description"] == property_data["description"]
        assert property_obj["price"] == property_data["price"]
        assert property_obj["owner_id"] == property_data["owner_id"]
        assert property_obj["status"] == "available"
        assert "_id" in property_obj

    @pytest.mark.asyncio
    async def test_get_property_by_id(self, test_client, test_property):
        """Test retrieving a property by ID."""
        response = test_client.get(f"/api/properties/{test_property['_id']}")
        
        assert response.status_code == 200
        property_obj = response.json()
        assert property_obj["_id"] == test_property["_id"]
        assert property_obj["title"] == test_property["title"]

    @pytest.mark.asyncio
    async def test_get_property_not_found(self, test_client):
        """Test retrieving a non-existent property."""
        response = test_client.get("/api/properties/000000000000000000000000")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_update_property(self, test_client, test_property, test_user):
        """Test updating a property."""
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "price": 1600.00
        }
        
        response = test_client.patch(
            f"/api/properties/{test_property['_id']}", 
            json=update_data,
            headers={"Authorization": f"Bearer {test_user.get('access_token', 'fake_token')}"}
        )
        
        assert response.status_code == 200
        property_obj = response.json()
        assert property_obj["title"] == update_data["title"]
        assert property_obj["description"] == update_data["description"]
        assert property_obj["price"] == update_data["price"]
        assert property_obj["address"] == test_property["address"]  # Unchanged field

    @pytest.mark.asyncio
    async def test_update_property_status(self, test_client, test_property, test_user):
        """Test updating a property's status."""
        update_data = {"status": "rented"}
        
        response = test_client.patch(
            f"/api/properties/{test_property['_id']}/status", 
            json=update_data,
            headers={"Authorization": f"Bearer {test_user.get('access_token', 'fake_token')}"}
        )
        
        assert response.status_code == 200
        property_obj = response.json()
        assert property_obj["status"] == update_data["status"]

    @pytest.mark.asyncio
    async def test_update_property_status_invalid(self, test_client, test_property, test_user):
        """Test updating a property's status with an invalid status."""
        update_data = {"status": "invalid_status"}
        
        response = test_client.patch(
            f"/api/properties/{test_property['_id']}/status", 
            json=update_data,
            headers={"Authorization": f"Bearer {test_user.get('access_token', 'fake_token')}"}
        )
        
        assert response.status_code == 400
        assert "invalid status" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_delete_property(self, test_client, test_property, test_user):
        """Test deleting a property."""
        response = test_client.delete(
            f"/api/properties/{test_property['_id']}",
            headers={"Authorization": f"Bearer {test_user.get('access_token', 'fake_token')}"}
        )
        
        assert response.status_code == 204
        
        # Verify the property is deleted
        get_response = test_client.get(f"/api/properties/{test_property['_id']}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_properties(self, test_client, test_property):
        """Test listing properties."""
        response = test_client.get("/api/properties")
        
        assert response.status_code == 200
        properties = response.json()
        assert isinstance(properties, list)
        assert len(properties) >= 1
        
        # Check if our test property is in the list
        property_ids = [prop["_id"] for prop in properties]
        assert test_property["_id"] in property_ids

    @pytest.mark.asyncio
    async def test_list_properties_with_filters(self, test_client, test_property):
        """Test listing properties with filters."""
        # Filter by property_type
        response = test_client.get(f"/api/properties?property_type={test_property['property_type']}")
        
        assert response.status_code == 200
        properties = response.json()
        assert isinstance(properties, list)
        for prop in properties:
            assert prop["property_type"] == test_property["property_type"]

    @pytest.mark.asyncio
    async def test_get_properties_by_owner(self, test_client, test_property, test_user):
        """Test retrieving properties by owner."""
        response = test_client.get(f"/api/properties/owner/{test_user['_id']}")
        
        assert response.status_code == 200
        properties = response.json()
        assert isinstance(properties, list)
        assert len(properties) >= 1
        for prop in properties:
            assert prop["owner_id"] == test_user["_id"]

    @pytest.mark.asyncio
    async def test_search_properties(self, test_client, test_property):
        """Test searching properties by text."""
        # Search for a term in the property title
        search_term = test_property["title"].split()[0]
        response = test_client.get(f"/api/properties/search?q={search_term}")
        
        assert response.status_code == 200
        properties = response.json()
        assert isinstance(properties, list)
        assert len(properties) >= 1
        
        # Our test property should be in the results
        property_ids = [prop["_id"] for prop in properties]
        assert test_property["_id"] in property_ids

    @pytest.mark.asyncio
    async def test_property_statistics(self, test_client, test_property):
        """Test retrieving property statistics."""
        response = test_client.get("/api/properties/statistics")
        
        assert response.status_code == 200
        stats = response.json()
        assert "total_properties" in stats
        assert "properties_by_status" in stats
        assert "properties_by_type" in stats
        assert stats["total_properties"] >= 1
        assert test_property["status"] in stats["properties_by_status"]
        assert test_property["property_type"] in stats["properties_by_type"] 