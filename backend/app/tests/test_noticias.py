import pytest
from fastapi.testclient import TestClient
from app.models.noticias import Noticia
from app.models.fuentes import Fuente
from app.models.categorias import Categoria
from app.models.user import User, StateUser
from datetime import datetime


def create_test_data(test_db):
    """Helper function to create test data"""
    # Create user
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
    
    # Create category
    categoria = Categoria(nombre="Tecnología", descripcion="Noticias de tecnología")
    test_db.add(categoria)
    test_db.commit()
    
    # Create source
    fuente = Fuente(nombre="TechNews", url="https://technews.com", descripcion="Portal de tecnología")
    test_db.add(fuente)
    test_db.commit()
    
    return user, categoria, fuente


def test_get_noticias_usuario_empty(client: TestClient, test_db):
    """Test getting user news when user has no news"""
    user, _, _ = create_test_data(test_db)
    
    response = client.get(f"/api/v1/noticias/usuario/{user.username}")
    assert response.status_code == 200
    assert response.json() == []


def test_get_noticias_usuario_with_data(client: TestClient, test_db):
    """Test getting user news with data"""
    user, categoria, fuente = create_test_data(test_db)
    
    # Create news
    noticia = Noticia(
        titulo="Nueva tecnología",
        resumen="Resumen de la noticia",
        enlace="https://example.com/news1",
        usuario=user.username,
        Id_Categoria=categoria.Id_Categoria,
        Id_Fuente=fuente.Id_Fuente,
        activa=1,
        etiquetas="tecnología,innovación"
    )
    test_db.add(noticia)
    test_db.commit()
    
    response = client.get(f"/api/v1/noticias/usuario/{user.username}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["titulo"] == "Nueva tecnología"
    assert data[0]["etiquetas"] == ["tecnología", "innovación"]


def test_update_noticia_success(client: TestClient, test_db):
    """Test successful news update"""
    user, categoria, fuente = create_test_data(test_db)
    
    # Create news
    noticia = Noticia(
        titulo="Título original",
        resumen="Resumen original",
        enlace="https://example.com/original",
        usuario=user.username,
        Id_Categoria=categoria.Id_Categoria,
        Id_Fuente=fuente.Id_Fuente,
        activa=1
    )
    test_db.add(noticia)
    test_db.commit()
    test_db.refresh(noticia)
    
    # Update news
    update_data = {
        "titulo": "Título actualizado",
        "resumen": "Resumen actualizado"
    }
    
    response = client.put(f"/api/v1/noticias/{noticia.Id_Noticia}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Título actualizado"
    assert data["resumen"] == "Resumen actualizado"


def test_update_noticia_not_found(client: TestClient, test_db):
    """Test update non-existent news"""
    update_data = {
        "titulo": "Título actualizado"
    }
    
    response = client.put("/api/v1/noticias/999", json=update_data)
    assert response.status_code == 404
    assert "Noticia no encontrada" in response.json()["detail"]


def test_inactivar_noticia_success(client: TestClient, test_db):
    """Test successful news deactivation"""
    user, categoria, fuente = create_test_data(test_db)
    
    # Create active news
    noticia = Noticia(
        titulo="Título test",
        resumen="Resumen test",
        enlace="https://example.com/test",
        usuario=user.username,
        Id_Categoria=categoria.Id_Categoria,
        Id_Fuente=fuente.Id_Fuente,
        activa=1
    )
    test_db.add(noticia)
    test_db.commit()
    test_db.refresh(noticia)
    
    response = client.patch(f"/api/v1/noticias/{noticia.Id_Noticia}/inactivar")
    assert response.status_code == 200
    data = response.json()
    assert data["activa"] == 0


def test_inactivar_noticia_not_found(client: TestClient, test_db):
    """Test deactivate non-existent news"""
    response = client.patch("/api/v1/noticias/999/inactivar")
    assert response.status_code == 404
    assert "Noticia no encontrada" in response.json()["detail"]


def test_get_all_noticias_empty(client: TestClient, test_db):
    """Test getting all news when database is empty"""
    response = client.get("/api/v1/noticias")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_noticias_with_data(client: TestClient, test_db):
    """Test getting all news with data"""
    user, categoria, fuente = create_test_data(test_db)
    
    # Create multiple news
    noticias = [
        Noticia(
            titulo="Noticia 1",
            resumen="Resumen 1",
            enlace="https://example.com/1",
            usuario=user.username,
            Id_Categoria=categoria.Id_Categoria,
            Id_Fuente=fuente.Id_Fuente,
            activa=1
        ),
        Noticia(
            titulo="Noticia 2",
            resumen="Resumen 2",
            enlace="https://example.com/2",
            usuario=user.username,
            Id_Categoria=categoria.Id_Categoria,
            Id_Fuente=fuente.Id_Fuente,
            activa=1
        )
    ]
    
    for noticia in noticias:
        test_db.add(noticia)
    test_db.commit()
    
    response = client.get("/api/v1/noticias")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_create_noticia_success(client: TestClient, test_db):
    """Test successful news creation"""
    user, categoria, fuente = create_test_data(test_db)
    
    noticia_data = {
        "titulo": "Nueva noticia",
        "resumen": "Resumen de la nueva noticia",
        "enlace": "https://example.com/nueva",
        "usuario": user.username,
        "Id_Categoria": categoria.Id_Categoria,
        "Id_Fuente": fuente.Id_Fuente,
        "etiquetas": "tag1,tag2,tag3"
    }
    
    response = client.post("/api/v1/noticias", json=noticia_data)
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Nueva noticia"
    assert data["usuario"] == user.username
    assert "Id_Noticia" in data


def test_create_noticia_missing_data(client: TestClient, test_db):
    """Test news creation with missing required data"""
    noticia_data = {
        "titulo": "Título incompleto"
        # Missing required fields
    }
    
    response = client.post("/api/v1/noticias", json=noticia_data)
    assert response.status_code == 422  # Validation error