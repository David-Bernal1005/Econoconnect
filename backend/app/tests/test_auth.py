import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.models.user import User, StateUser
from app.core.security import get_password_hash


def test_register_success(client: TestClient, test_db):
    """Test successful user registration"""
    user_data = {
        "name": "Juan",
        "lastname": "Pérez",
        "cellphone": "+1234567890",
        "direction": "Calle 123",
        "username": "juan_perez",
        "password": "password123",
        "rol": "usuario",
        "country": "Colombia",
        "email": "juan@example.com"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "juan_perez"
    assert data["email"] == "juan@example.com"
    assert "id_user" in data


def test_register_duplicate_username(client: TestClient, test_db):
    """Test registration with duplicate username"""
    user_data = {
        "name": "Juan",
        "lastname": "Pérez",
        "cellphone": "+1234567890",
        "direction": "Calle 123",
        "username": "juan_perez",
        "password": "password123",
        "rol": "usuario",
        "country": "Colombia",
        "email": "juan@example.com"
    }
    
    # First registration
    client.post("/api/v1/auth/register", json=user_data)
    
    # Second registration with same username
    user_data["email"] = "juan2@example.com"
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "username ya existe" in response.json()["detail"]


def test_register_duplicate_email(client: TestClient, test_db):
    """Test registration with duplicate email"""
    user_data = {
        "name": "Juan",
        "lastname": "Pérez",
        "cellphone": "+1234567890",
        "direction": "Calle 123",
        "username": "juan_perez",
        "password": "password123",
        "rol": "usuario",
        "country": "Colombia",
        "email": "juan@example.com"
    }
    
    # First registration
    client.post("/api/v1/auth/register", json=user_data)
    
    # Second registration with same email
    user_data["username"] = "juan_perez2"
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "email ya existe" in response.json()["detail"]


def test_login_success(client: TestClient, test_db):
    """Test successful login"""
    # First register a user
    user_data = {
        "name": "Juan",
        "lastname": "Pérez",
        "cellphone": "+1234567890",
        "direction": "Calle 123",
        "username": "juan_perez",
        "password": "password123",
        "rol": "usuario",
        "country": "Colombia",
        "email": "juan@example.com"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Now login
    login_data = {
        "username": "juan_perez",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["name"] == "Juan"


def test_login_invalid_credentials(client: TestClient, test_db):
    """Test login with invalid credentials"""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Credenciales incorrectas" in response.json()["detail"]


@patch('app.api.v1.endpoints.auth.send_email')
def test_forgot_password_success(mock_send_email, client: TestClient, test_db):
    """Test successful password reset request"""
    # First register a user
    user_data = {
        "name": "Juan",
        "lastname": "Pérez",
        "cellphone": "+1234567890",
        "direction": "Calle 123",
        "username": "juan_perez",
        "password": "password123",
        "rol": "usuario",
        "country": "Colombia",
        "email": "juan@example.com"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Request password reset
    reset_data = {"email": "juan@example.com"}
    response = client.post("/api/v1/auth/forgot-password", json=reset_data)
    assert response.status_code == 200
    assert "código a tu correo" in response.json()["msg"]
    mock_send_email.assert_called_once()


def test_forgot_password_user_not_found(client: TestClient, test_db):
    """Test password reset request for non-existent user"""
    reset_data = {"email": "nonexistent@example.com"}
    response = client.post("/api/v1/auth/forgot-password", json=reset_data)
    assert response.status_code == 404
    assert "No encontramos tu usuario" in response.json()["detail"]


@patch('app.api.v1.endpoints.auth.reset_codes', {"juan@example.com": ("123456", 1000000000)})
def test_reset_password_success(client: TestClient, test_db):
    """Test successful password reset"""
    # First register a user
    user_data = {
        "name": "Juan",
        "lastname": "Pérez",
        "cellphone": "+1234567890",
        "direction": "Calle 123",
        "username": "juan_perez",
        "password": "password123",
        "rol": "usuario",
        "country": "Colombia",
        "email": "juan@example.com"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Reset password
    with patch('time.time', return_value=1000000060):  # 1 minute later
        reset_data = {
            "email": "juan@example.com",
            "code": "123456",
            "new_password": "newpassword123"
        }
        response = client.post("/api/v1/auth/reset-password", json=reset_data)
        assert response.status_code == 200
        assert "Contraseña actualizada" in response.json()["msg"]


def test_reset_password_invalid_code(client: TestClient, test_db):
    """Test password reset with invalid code"""
    # First register a user
    user_data = {
        "name": "Juan",
        "lastname": "Pérez",
        "cellphone": "+1234567890",
        "direction": "Calle 123",
        "username": "juan_perez",
        "password": "password123",
        "rol": "usuario",
        "country": "Colombia",
        "email": "juan@example.com"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Reset password with wrong code
    with patch('app.api.v1.endpoints.auth.reset_codes', {"juan@example.com": ("123456", 1000000000)}):
        with patch('time.time', return_value=1000000060):
            reset_data = {
                "email": "juan@example.com",
                "code": "654321",  # Wrong code
                "new_password": "newpassword123"
            }
            response = client.post("/api/v1/auth/reset-password", json=reset_data)
            assert response.status_code == 400
            assert "Código inválido" in response.json()["detail"]


def test_reset_password_expired_code(client: TestClient, test_db):
    """Test password reset with expired code"""
    # First register a user
    user_data = {
        "name": "Juan",
        "lastname": "Pérez",
        "cellphone": "+1234567890",
        "direction": "Calle 123",
        "username": "juan_perez",
        "password": "password123",
        "rol": "usuario",
        "country": "Colombia",
        "email": "juan@example.com"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # Reset password with expired code
    with patch('app.api.v1.endpoints.auth.reset_codes', {"juan@example.com": ("123456", 1000000000)}):
        with patch('time.time', return_value=1000000300):  # 5 minutes later (expired)
            reset_data = {
                "email": "juan@example.com",
                "code": "123456",
                "new_password": "newpassword123"
            }
            response = client.post("/api/v1/auth/reset-password", json=reset_data)
            assert response.status_code == 400
            assert "código ha expirado" in response.json()["detail"]