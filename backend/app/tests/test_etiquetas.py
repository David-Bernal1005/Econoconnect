import pytest
from fastapi.testclient import TestClient
from app.models.etiqueta import Etiqueta
from app.models.user import User, StateUser
from datetime import datetime


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


def test_get_etiquetas_empty(client: TestClient, test_db):
    """Test getting tags when database is empty"""
    response = client.get("/api/v1/etiquetas")
    assert response.status_code == 200
    assert response.json() == []


def test_get_etiquetas_with_data(client: TestClient, test_db):
    """Test getting tags with data"""
    user = create_test_user(test_db)
    
    # Create test tags
    etiquetas = [
        Etiqueta(
            nombre="Tecnología",
            descripcion="Etiqueta para temas de tecnología",
            autor_id=user.id_user,
            estado="activa",
            fecha_creacion=datetime.now()
        ),
        Etiqueta(
            nombre="Economía",
            descripcion="Etiqueta para temas económicos",
            autor_id=user.id_user,
            estado="activa",
            fecha_creacion=datetime.now()
        ),
        Etiqueta(
            nombre="Política",
            descripcion="Etiqueta para temas políticos",
            autor_id=user.id_user,
            estado="inactiva",
            fecha_creacion=datetime.now()
        )
    ]
    
    for etiqueta in etiquetas:
        test_db.add(etiqueta)
    test_db.commit()
    
    response = client.get("/api/v1/etiquetas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Verify tag names
    nombres = [tag["nombre"] for tag in data]
    assert "Tecnología" in nombres
    assert "Economía" in nombres
    assert "Política" in nombres


def test_get_etiquetas_response_structure(client: TestClient, test_db):
    """Test the structure of tags response"""
    user = create_test_user(test_db)
    
    etiqueta = Etiqueta(
        nombre="Test Tag",
        descripcion="Tag de prueba",
        autor_id=user.id_user,
        estado="activa",
        fecha_creacion=datetime.now()
    )
    test_db.add(etiqueta)
    test_db.commit()
    
    response = client.get("/api/v1/etiquetas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    
    tag = data[0]
    # Verify all expected fields are present
    assert "id_etiqueta" in tag
    assert "nombre" in tag
    assert "descripcion" in tag
    assert "autor_id" in tag
    assert "estado" in tag
    assert "fecha_creacion" in tag
    
    # Verify values
    assert tag["nombre"] == "Test Tag"
    assert tag["descripcion"] == "Tag de prueba"
    assert tag["autor_id"] == user.id_user
    assert tag["estado"] == "activa"


def test_get_etiquetas_different_states(client: TestClient, test_db):
    """Test getting tags with different states"""
    user = create_test_user(test_db)
    
    # Create tags with different states
    etiquetas = [
        Etiqueta(
            nombre="Activa 1",
            descripcion="Etiqueta activa 1",
            autor_id=user.id_user,
            estado="activa",
            fecha_creacion=datetime.now()
        ),
        Etiqueta(
            nombre="Inactiva 1",
            descripcion="Etiqueta inactiva 1",
            autor_id=user.id_user,
            estado="inactiva",
            fecha_creacion=datetime.now()
        ),
        Etiqueta(
            nombre="Pendiente 1",
            descripcion="Etiqueta pendiente 1",
            autor_id=user.id_user,
            estado="pendiente",
            fecha_creacion=datetime.now()
        )
    ]
    
    for etiqueta in etiquetas:
        test_db.add(etiqueta)
    test_db.commit()
    
    response = client.get("/api/v1/etiquetas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Verify all states are returned
    estados = [tag["estado"] for tag in data]
    assert "activa" in estados
    assert "inactiva" in estados
    assert "pendiente" in estados


def test_get_etiquetas_fecha_creacion_format(client: TestClient, test_db):
    """Test that fecha_creacion is returned as string"""
    user = create_test_user(test_db)
    
    etiqueta = Etiqueta(
        nombre="Test Date",
        descripcion="Test date format",
        autor_id=user.id_user,
        estado="activa",
        fecha_creacion=datetime.now()
    )
    test_db.add(etiqueta)
    test_db.commit()
    
    response = client.get("/api/v1/etiquetas")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    
    tag = data[0]
    assert isinstance(tag["fecha_creacion"], str)
    # Verify it's a valid datetime string representation
    datetime.fromisoformat(tag["fecha_creacion"].replace("Z", "+00:00"))