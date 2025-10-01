import pytest
from fastapi.testclient import TestClient
from app.models.user import User, StateUser
from app.core.security import create_access_token


def create_test_user(test_db):
    """Helper function to create a test user"""
    user = User(
        name="Juan",
        lastname="Pérez",
        cellphone="+1234567890",
        direction="Calle 123",
        username="juan_perez",
        hashed_password="hashed_password",
        rol="usuario",
        country="Colombia",
        email="juan@example.com",
        state=StateUser.activo,
        number_followers=0
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


def create_auth_headers(username: str, rol: str = "usuario"):
    """Helper function to create auth headers"""
    token = create_access_token({"sub": username, "rol": rol})
    return {"Authorization": f"Bearer {token}"}


def test_get_current_user_success(client: TestClient, test_db):
    """Test successful user profile retrieval"""
    user = create_test_user(test_db)
    headers = create_auth_headers(user.username)
    
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "juan_perez"
    assert data["email"] == "juan@example.com"
    assert data["name"] == "Juan"


def test_get_current_user_no_token(client: TestClient, test_db):
    """Test user profile retrieval without token"""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


def test_get_current_user_invalid_token(client: TestClient, test_db):
    """Test user profile retrieval with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401


def test_get_current_user_nonexistent_user(client: TestClient, test_db):
    """Test user profile retrieval for non-existent user"""
    headers = create_auth_headers("nonexistent_user")
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401