import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import UserCreate
from unittest.mock import AsyncMock, patch

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_user():
    with patch("app.routers.users.users_collection.insert_one") as mock_insert, \
         patch("app.routers.users.users_collection.find_one") as mock_find:

        mock_insert.return_value = AsyncMock(inserted_id="507f1f77bcf86cd799439011")
        mock_find.return_value = {
            "_id": "507f1f77bcf86cd799439011",
            "name": "John Doe",
            "email": "john@example.com"
        }

        user_data = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        assert response.json()["id"] == "507f1f77bcf86cd799439011"