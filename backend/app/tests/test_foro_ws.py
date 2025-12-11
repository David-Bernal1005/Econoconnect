import pytest
from fastapi.testclient import TestClient
from app.models.user import User, StateUser
from app.models.foro import Foro, EstadoForo
from app.models.comentarioforo import Comentario
from app.core.security import create_access_token
from datetime import datetime
import asyncio


def create_test_user(test_db, username: str, email: str) -> User:
    user = User(
        name="Test",
        lastname="User",
        cellphone="+123456789",
        direction="Calle 123",
        username=username,
        hashed_password="hashed_password",
        rol="usuario",
        country="Colombia",
        email=email,
        state=StateUser.activo,
        number_followers=0,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


def create_auth_headers(username: str, rol: str = "usuario") -> dict:
    token = create_access_token({"sub": username, "rol": rol})
    return {"Authorization": f"Bearer {token}"}


def test_get_comentarios_foro_vacio(client: TestClient, test_db):
    """GET /ws/foro/{id}/comentarios devuelve lista vacía si no hay comentarios."""
    user = create_test_user(test_db, "autor", "autor@example.com")
    foro = Foro(nombre="Foro", descripcion="d", autor_id=user.id_user, estado=EstadoForo.activo)
    test_db.add(foro)
    test_db.commit()
    test_db.refresh(foro)

    resp = client.get(f"/ws/foro/{foro.id_foro}/comentarios")
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_comentarios_foro_no_existe(client: TestClient, test_db):
    """GET /ws/foro/{id}/comentarios con foro inexistente devuelve 404."""
    resp = client.get("/ws/foro/999/comentarios")
    assert resp.status_code == 404


def test_crear_comentario_rest_ok(client: TestClient, test_db):
    """POST /ws/foro/{id}/comentarios crea comentario con token válido."""
    user = create_test_user(test_db, "autor", "autor@example.com")
    foro = Foro(nombre="Foro", descripcion="d", autor_id=user.id_user, estado=EstadoForo.activo)
    test_db.add(foro)
    test_db.commit()
    test_db.refresh(foro)

    token = create_access_token({"sub": user.username, "rol": "usuario"})
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post(
        f"/ws/foro/{foro.id_foro}/comentarios",
        json={"contenido": "Hola mundo"},
        headers=headers,
    )

    assert resp.status_code == 201
    data = resp.json()
    assert data["contenido"] == "Hola mundo"
    assert data["id_user"] == user.id_user

    comentario_db = (
        test_db.query(Comentario)
        .filter_by(id_foro=foro.id_foro, id_user=user.id_user)
        .first()
    )
    assert comentario_db is not None


def test_crear_comentario_rest_no_autenticado(client: TestClient, test_db):
    """Crear comentario sin token devuelve 401."""
    user = create_test_user(test_db, "autor", "autor@example.com")
    foro = Foro(nombre="Foro", descripcion="d", autor_id=user.id_user, estado=EstadoForo.activo)
    test_db.add(foro)
    test_db.commit()
    test_db.refresh(foro)

    resp = client.post(
        f"/ws/foro/{foro.id_foro}/comentarios",
        json={"contenido": "Hola"},
    )

    # HTTPBearer sin credenciales responde 403 (Forbidden)
    assert resp.status_code == 403


def test_crear_comentario_rest_foro_no_encontrado(client: TestClient, test_db):
    """Crear comentario para foro inexistente devuelve 404."""
    user = create_test_user(test_db, "autor", "autor@example.com")
    token = create_access_token({"sub": user.username, "rol": "usuario"})
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post(
        "/ws/foro/999/comentarios",
        json={"contenido": "Hola"},
        headers=headers,
    )

    assert resp.status_code == 404


def test_websocket_conexion_basica(client: TestClient, test_db):
    """Conexión WebSocket básica con token válido (no valida broadcast)."""
    user = create_test_user(test_db, "autor", "autor@example.com")
    foro = Foro(nombre="Foro", descripcion="d", autor_id=user.id_user, estado=EstadoForo.activo)
    test_db.add(foro)
    test_db.commit()
    test_db.refresh(foro)

    token = create_access_token({"sub": user.username, "rol": "usuario"})

    # La conexión WebSocket con TestClient ya es síncrona, no requiere pytest-asyncio.
    with client.websocket_connect(f"/ws/foro/{foro.id_foro}?token={token}") as websocket:
        websocket.send_text('{"contenido": "mensaje"}')
