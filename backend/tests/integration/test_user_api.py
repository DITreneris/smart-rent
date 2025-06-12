"""
Integration tests for User API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestUserAPI:
    """Test cases for the User API endpoints."""

    @pytest.mark.asyncio
    async def test_create_user(self, test_client, test_user_data, empty_test_database):
        """Test creating a new user."""
        response = test_client.post("/api/users", json=test_user_data)
        
        assert response.status_code == 201
        user = response.json()
        assert user["email"] == test_user_data["email"]
        assert user["first_name"] == test_user_data["first_name"]
        assert user["last_name"] == test_user_data["last_name"]
        assert user["role"] == test_user_data["role"]
        assert user["wallet_address"] == test_user_data["wallet_address"]
        assert "_id" in user
        assert "password" not in user  # Password should not be returned

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, test_client, test_user, test_user_data):
        """Test creating a user with a duplicate email."""
        response = test_client.post("/api/users", json=test_user_data)
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_create_user_duplicate_wallet(self, test_client, test_user, test_user_data):
        """Test creating a user with a duplicate wallet address."""
        # Update email but keep the same wallet address
        modified_data = dict(test_user_data)
        modified_data["email"] = "unique@example.com"
        
        response = test_client.post("/api/users", json=modified_data)
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, test_client, test_user):
        """Test retrieving a user by ID."""
        response = test_client.get(f"/api/users/{test_user['_id']}")
        
        assert response.status_code == 200
        user = response.json()
        assert user["_id"] == test_user["_id"]
        assert user["email"] == test_user["email"]

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, test_client):
        """Test retrieving a non-existent user."""
        response = test_client.get("/api/users/000000000000000000000000")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_update_user(self, test_client, test_user):
        """Test updating a user."""
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }
        
        response = test_client.patch(
            f"/api/users/{test_user['_id']}", 
            json=update_data,
            headers={"Authorization": f"Bearer {test_user.get('access_token', 'fake_token')}"}
        )
        
        assert response.status_code == 200
        user = response.json()
        assert user["first_name"] == update_data["first_name"]
        assert user["last_name"] == update_data["last_name"]
        assert user["email"] == test_user["email"]  # Unchanged field

    @pytest.mark.asyncio
    async def test_update_user_role(self, test_client, test_user):
        """Test updating a user's role."""
        update_data = {"role": "landlord"}
        
        response = test_client.patch(
            f"/api/users/{test_user['_id']}/role", 
            json=update_data,
            headers={"Authorization": f"Bearer {test_user.get('access_token', 'fake_token')}"}
        )
        
        assert response.status_code == 200
        user = response.json()
        assert user["role"] == update_data["role"]

    @pytest.mark.asyncio
    async def test_update_user_role_invalid(self, test_client, test_user):
        """Test updating a user's role with an invalid role."""
        update_data = {"role": "invalid_role"}
        
        response = test_client.patch(
            f"/api/users/{test_user['_id']}/role", 
            json=update_data,
            headers={"Authorization": f"Bearer {test_user.get('access_token', 'fake_token')}"}
        )
        
        assert response.status_code == 400
        assert "invalid role" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_delete_user(self, test_client, test_user):
        """Test deleting a user."""
        response = test_client.delete(
            f"/api/users/{test_user['_id']}",
            headers={"Authorization": f"Bearer {test_user.get('access_token', 'fake_token')}"}
        )
        
        assert response.status_code == 204
        
        # Verify the user is deleted
        get_response = test_client.get(f"/api/users/{test_user['_id']}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_users(self, test_client, test_user):
        """Test listing users."""
        response = test_client.get("/api/users")
        
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) >= 1
        
        # Check if our test user is in the list
        user_ids = [user["_id"] for user in users]
        assert test_user["_id"] in user_ids

    @pytest.mark.asyncio
    async def test_list_users_with_filters(self, test_client, test_user):
        """Test listing users with filters."""
        # Filter by role
        response = test_client.get(f"/api/users?role={test_user['role']}")
        
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        for user in users:
            assert user["role"] == test_user["role"]

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, test_client, test_user):
        """Test retrieving a user by email."""
        response = test_client.get(f"/api/users/email/{test_user['email']}")
        
        assert response.status_code == 200
        user = response.json()
        assert user["email"] == test_user["email"]
        assert user["_id"] == test_user["_id"]

    @pytest.mark.asyncio
    async def test_get_user_by_wallet(self, test_client, test_user):
        """Test retrieving a user by wallet address."""
        response = test_client.get(f"/api/users/wallet/{test_user['wallet_address']}")
        
        assert response.status_code == 200
        user = response.json()
        assert user["wallet_address"] == test_user["wallet_address"]
        assert user["_id"] == test_user["_id"]

    @pytest.mark.asyncio
    async def test_user_statistics(self, test_client, test_user):
        """Test retrieving user statistics."""
        response = test_client.get("/api/users/statistics")
        
        assert response.status_code == 200
        stats = response.json()
        assert "total_users" in stats
        assert "users_by_role" in stats
        assert stats["total_users"] >= 1
        assert test_user["role"] in stats["users_by_role"] 