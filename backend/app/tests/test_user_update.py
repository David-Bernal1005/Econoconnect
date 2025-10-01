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


def test_update_user_success(client: TestClient, test_db):
    """Test successful user update"""
    user = create_test_user(test_db)
    headers = create_auth_headers(user.username)
    
    update_data = {
        "name": "Juan Carlos",
        "lastname": "Pérez González",
        "email": "juan.carlos@example.com",
        "cellphone": "+1234567891",
        "direction": "Calle 456"
    }
    
    response = client.put("/api/v1/users/me", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Juan Carlos"
    assert data["lastname"] == "Pérez González"
    assert data["email"] == "juan.carlos@example.com"


def test_update_user_no_token(client: TestClient, test_db):
    """Test user update without token"""
    update_data = {
        "name": "Juan Carlos",
        "lastname": "Pérez González",
        "email": "juan.carlos@example.com",
        "cellphone": "+1234567891",
        "direction": "Calle 456"
    }
    
    response = client.put("/api/v1/users/me", json=update_data)
    assert response.status_code == 401


def test_update_user_invalid_token(client: TestClient, test_db):
    """Test user update with invalid token"""
    update_data = {
        "name": "Juan Carlos",
        "lastname": "Pérez González",
        "email": "juan.carlos@example.com",
        "cellphone": "+1234567891",
        "direction": "Calle 456"
    }
    
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.put("/api/v1/users/me", json=update_data, headers=headers)
    assert response.status_code == 401


def test_update_user_partial_data(client: TestClient, test_db):
    """Test user update with partial data"""
    user = create_test_user(test_db)
    headers = create_auth_headers(user.username)
    
    update_data = {
        "name": "Juan Carlos"
    }
    
    response = client.put("/api/v1/users/me", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Juan Carlos"
    # Other fields should remain unchanged
    assert data["lastname"] == "Pérez"