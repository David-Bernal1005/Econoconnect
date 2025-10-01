import pytest
from fastapi.testclient import TestClient
from app.models.datografica import DatoGrafica


def test_get_graficas_empty(client: TestClient, test_db):
    """Test getting graphics data when database is empty"""
    response = client.get("/api/v1/graficas")
    assert response.status_code == 200
    assert response.json() == []


def test_get_graficas_with_data(client: TestClient, test_db):
    """Test getting graphics data with sample data"""
    # Create test graphic data
    datos = [
        DatoGrafica(nombre="Enero", valor=100.0),
        DatoGrafica(nombre="Febrero", valor=150.0),
        DatoGrafica(nombre="Marzo", valor=120.0),
        DatoGrafica(nombre="Abril", valor=180.0),
        DatoGrafica(nombre="Mayo", valor=200.0)
    ]
    
    for dato in datos:
        test_db.add(dato)
    test_db.commit()
    
    response = client.get("/api/v1/graficas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    
    # Verify data structure
    for item in data:
        assert "name" in item
        assert "value" in item
    
    # Verify specific values
    names = [item["name"] for item in data]
    values = [item["value"] for item in data]
    
    assert "Enero" in names
    assert "Febrero" in names
    assert "Marzo" in names
    assert "Abril" in names
    assert "Mayo" in names
    
    assert 100.0 in values
    assert 150.0 in values
    assert 120.0 in values
    assert 180.0 in values
    assert 200.0 in values


def test_get_graficas_response_structure(client: TestClient, test_db):
    """Test the structure of graphics response"""
    # Create a single test data point
    dato = DatoGrafica(nombre="Test Data", valor=250.5)
    test_db.add(dato)
    test_db.commit()
    
    response = client.get("/api/v1/graficas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    
    item = data[0]
    assert item["name"] == "Test Data"
    assert item["value"] == 250.5


def test_get_graficas_multiple_types(client: TestClient, test_db):
    """Test graphics data with different types of data"""
    # Create test data with different value types
    datos = [
        DatoGrafica(nombre="Ventas", valor=1500.75),
        DatoGrafica(nombre="Usuarios", valor=42),
        DatoGrafica(nombre="Conversión", valor=3.14),
        DatoGrafica(nombre="Gastos", valor=999.99)
    ]
    
    for dato in datos:
        test_db.add(dato)
    test_db.commit()
    
    response = client.get("/api/v1/graficas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    
    # Verify all items have correct structure
    for item in data:
        assert isinstance(item["name"], str)
        assert isinstance(item["value"], (int, float))


def test_get_graficas_zero_values(client: TestClient, test_db):
    """Test graphics data with zero and negative values"""
    # Create test data with edge cases
    datos = [
        DatoGrafica(nombre="Zero", valor=0.0),
        DatoGrafica(nombre="Negative", valor=-100.0),
        DatoGrafica(nombre="Small", valor=0.001)
    ]
    
    for dato in datos:
        test_db.add(dato)
    test_db.commit()
    
    response = client.get("/api/v1/graficas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Find specific items
    zero_item = next(item for item in data if item["name"] == "Zero")
    negative_item = next(item for item in data if item["name"] == "Negative")
    small_item = next(item for item in data if item["name"] == "Small")
    
    assert zero_item["value"] == 0.0
    assert negative_item["value"] == -100.0
    assert small_item["value"] == 0.001