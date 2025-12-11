import pytest
from fastapi.testclient import TestClient
from app.models.user import User, StateUser
from app.models.foro import Foro, EstadoForo
from app.core.security import create_access_token


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


def test_crear_foro_ok(client: TestClient, test_db):
    """POST /api/v1/foro crea un foro asociado al usuario autenticado."""
    user = create_test_user(test_db, "autor", "autor@example.com")
    headers = create_auth_headers(user.username)

    payload = {"nombre": "Foro de prueba", "descripcion": "desc", "id_grafica": None}
    resp = client.post("/api/v1/foro", json=payload, headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["nombre"] == "Foro de prueba"
    assert data["autor_id"] == user.id_user
    assert data["autor_username"] == user.username


def test_crear_foro_no_autenticado(client: TestClient, test_db):
    """Crear foro sin token devuelve 401."""
    payload = {"nombre": "Foro de prueba", "descripcion": "desc", "id_grafica": None}
    resp = client.post("/api/v1/foro", json=payload)

    assert resp.status_code == 401


def test_listar_foros(client: TestClient, test_db):
    """GET /api/v1/foro lista solo foros activos."""
    user = create_test_user(test_db, "autor", "autor@example.com")
    headers = create_auth_headers(user.username)

    # Crear dos foros
    f1 = Foro(nombre="F1", descripcion="d1", autor_id=user.id_user, estado=EstadoForo.activo)
    f2 = Foro(nombre="F2", descripcion="d2", autor_id=user.id_user, estado=EstadoForo.inactivo)
    test_db.add_all([f1, f2])
    test_db.commit()

    resp = client.get("/api/v1/foro", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    names = {f["nombre"] for f in data}
    assert "F1" in names
    assert "F2" not in names


def test_obtener_foro_no_encontrado(client: TestClient, test_db):
    """GET /api/v1/foro/{id} con ID inexistente devuelve 404."""
    user = create_test_user(test_db, "autor", "autor@example.com")
    headers = create_auth_headers(user.username)

    resp = client.get("/api/v1/foro/999", headers=headers)
    assert resp.status_code == 404
    assert "Foro no encontrado" in resp.json()["detail"]


def test_eliminar_foro_por_autor(client: TestClient, test_db):
    """El autor puede marcar su foro como inactivo (delete lógico)."""
    user = create_test_user(test_db, "autor", "autor@example.com")
    headers = create_auth_headers(user.username)

    foro = Foro(nombre="F1", descripcion="d1", autor_id=user.id_user, estado=EstadoForo.activo)
    test_db.add(foro)
    test_db.commit()
    test_db.refresh(foro)

    resp = client.delete(f"/api/v1/foro/{foro.id_foro}", headers=headers)
    assert resp.status_code == 200
    assert "Foro eliminado correctamente" in resp.json()["message"]

    test_db.refresh(foro)
    assert foro.estado == EstadoForo.inactivo


def test_eliminar_foro_por_otro_usuario_forbidden(client: TestClient, test_db):
    """Un usuario que no es autor no puede eliminar el foro (403)."""
    autor = create_test_user(test_db, "autor", "autor@example.com")
    otro = create_test_user(test_db, "otro", "otro@example.com")

    foro = Foro(nombre="F1", descripcion="d1", autor_id=autor.id_user, estado=EstadoForo.activo)
    test_db.add(foro)
    test_db.commit()
    test_db.refresh(foro)

    headers = create_auth_headers(otro.username)
    resp = client.delete(f"/api/v1/foro/{foro.id_foro}", headers=headers)

    assert resp.status_code == 403
    assert "No tienes permiso" in resp.json()["detail"]
