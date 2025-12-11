import pytest
from fastapi.testclient import TestClient
from app.models.publicacion import Publicacion
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


def test_get_publicaciones_empty(client: TestClient, test_db):
    """Test getting publications when database is empty"""
    response = client.get("/api/v1/publicaciones")
    assert response.status_code == 200
    assert response.json() == []


def test_get_publicaciones_with_data(client: TestClient, test_db):
    """Test getting publications with data"""
    user = create_test_user(test_db)
    
    # Create test publications
    publicaciones = [
        Publicacion(
            titulo="Publicación 1",
            contenido="Contenido de la primera publicación",
            id_user=user.id_user,
        ),
        Publicacion(
            titulo="Publicación 2",
            contenido="Contenido de la segunda publicación",
            id_user=user.id_user,
        ),
        Publicacion(
            titulo="Publicación 3",
            contenido="Contenido de la tercera publicación",
            id_user=user.id_user,
        )
    ]
    
    for pub in publicaciones:
        test_db.add(pub)
    test_db.commit()
    
    response = client.get("/api/v1/publicaciones")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Verify publication data
    titles = [pub["titulo"] for pub in data]
    assert "Publicación 1" in titles
    assert "Publicación 2" in titles
    assert "Publicación 3" in titles


def test_get_publicaciones_structure(client: TestClient, test_db):
    """Test the structure of publication response"""
    user = create_test_user(test_db)
    
    publicacion = Publicacion(
        titulo="Test Publication",
        contenido="Test content",
        id_user=user.id_user,
    )
    test_db.add(publicacion)
    test_db.commit()
    
    response = client.get("/api/v1/publicaciones")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    
    pub = data[0]
    assert "titulo" in pub
    assert "contenido" in pub
    assert "id_user" in pub
    assert "fecha_creacion" in pub
    assert pub["titulo"] == "Test Publication"
    assert pub["contenido"] == "Test content"