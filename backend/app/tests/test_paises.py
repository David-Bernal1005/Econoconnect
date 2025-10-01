import pytest
from fastapi.testclient import TestClient
from app.models.paises import Pais


def test_get_paises_empty(client: TestClient, test_db):
    """Test getting countries when database is empty"""
    response = client.get("/api/v1/paises")
    assert response.status_code == 200
    assert response.json() == []


def test_get_paises_with_data(client: TestClient, test_db):
    """Test getting countries with data"""
    # Create test countries
    pais1 = Pais(nombre="Colombia", codigo_iso="CO", codigo_telefono="+57")
    pais2 = Pais(nombre="Argentina", codigo_iso="AR", codigo_telefono="+54")
    test_db.add(pais1)
    test_db.add(pais2)
    test_db.commit()
    
    response = client.get("/api/v1/paises")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Check if countries are ordered by name
    country_names = [country["nombre"] for country in data]
    assert country_names == ["Argentina", "Colombia"]


def test_create_pais_success(client: TestClient, test_db):
    """Test successful country creation"""
    pais_data = {
        "nombre": "México",
        "codigo_iso": "MX",
        "codigo_telefono": "+52"
    }
    
    response = client.post("/api/v1/paises", json=pais_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "México"
    assert data["codigo_iso"] == "MX"
    assert data["codigo_telefono"] == "+52"
    assert "id_pais" in data


def test_create_pais_minimal_data(client: TestClient, test_db):
    """Test country creation with minimal data"""
    pais_data = {
        "nombre": "Brasil"
    }
    
    response = client.post("/api/v1/paises", json=pais_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Brasil"
    assert data["codigo_iso"] is None
    assert data["codigo_telefono"] is None


def test_create_pais_invalid_data(client: TestClient, test_db):
    """Test country creation with invalid data"""
    pais_data = {}  # Empty data
    
    response = client.post("/api/v1/paises", json=pais_data)
    # This might return 422 for validation error or 500 for server error
    assert response.status_code in [422, 500]


def test_get_paises_after_creation(client: TestClient, test_db):
    """Test getting countries after creating some"""
    # Create countries
    countries = [
        {"nombre": "Venezuela", "codigo_iso": "VE", "codigo_telefono": "+58"},
        {"nombre": "Chile", "codigo_iso": "CL", "codigo_telefono": "+56"},
        {"nombre": "Perú", "codigo_iso": "PE", "codigo_telefono": "+51"}
    ]
    
    for country in countries:
        client.post("/api/v1/paises", json=country)
    
    # Get all countries
    response = client.get("/api/v1/paises")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Verify alphabetical order
    country_names = [country["nombre"] for country in data]
    assert country_names == ["Chile", "Perú", "Venezuela"]