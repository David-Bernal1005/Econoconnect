import pytest
from fastapi.testclient import TestClient
from app.models.user import User, StateUser
from app.models.usuarioseguido import UsuarioSeguido
from app.core.security import create_access_token


def create_test_user(test_db, username: str, email: str) -> User:
    """Crea un usuario de prueba básico."""
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
    """Genera headers Authorization Bearer para un usuario."""
    token = create_access_token({"sub": username, "rol": rol})
    return {"Authorization": f"Bearer {token}"}


def test_sugerencias_excluye_usuario_actual(client: TestClient, test_db):
    """GET /api/v1/seguidores/sugerencias devuelve otros usuarios y nunca al actual."""
    current = create_test_user(test_db, "user_actual", "actual@example.com")
    u1 = create_test_user(test_db, "user1", "u1@example.com")
    u2 = create_test_user(test_db, "user2", "u2@example.com")

    headers = create_auth_headers(current.username)
    resp = client.get("/api/v1/seguidores/sugerencias", headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    usernames = {u["username"] for u in data}
    assert current.username not in usernames
    assert {u1.username, u2.username}.issubset(usernames)


def test_seguir_usuario_ok(client: TestClient, test_db):
    """POST /api/v1/seguidores/seguir crea la relación si no existe."""
    current = create_test_user(test_db, "user_actual", "actual@example.com")
    target = create_test_user(test_db, "user_target", "target@example.com")

    headers = create_auth_headers(current.username)
    resp = client.post(
        "/api/v1/seguidores/seguir",
        json={"id_user_seguido": target.id_user},
        headers=headers,
    )

    assert resp.status_code == 200
    assert "Usuario seguido correctamente" in resp.json()["message"]

    rel = (
        test_db.query(UsuarioSeguido)
        .filter_by(id_user=current.id_user, id_user_seguido=target.id_user)
        .first()
    )
    assert rel is not None


def test_seguir_usuario_a_si_mismo(client: TestClient, test_db):
    """No se permite seguirse a sí mismo (400)."""
    current = create_test_user(test_db, "user_actual", "actual@example.com")
    headers = create_auth_headers(current.username)

    resp = client.post(
        "/api/v1/seguidores/seguir",
        json={"id_user_seguido": current.id_user},
        headers=headers,
    )

    assert resp.status_code == 400
    assert "No puedes seguirte a ti mismo" in resp.json()["detail"]


def test_seguir_usuario_duplicado(client: TestClient, test_db):
    """Intentar seguir dos veces al mismo usuario devuelve 400."""
    current = create_test_user(test_db, "user_actual", "actual@example.com")
    target = create_test_user(test_db, "user_target", "target@example.com")
    headers = create_auth_headers(current.username)

    # Primera vez OK
    client.post(
        "/api/v1/seguidores/seguir",
        json={"id_user_seguido": target.id_user},
        headers=headers,
    )

    # Segunda vez debe fallar
    resp = client.post(
        "/api/v1/seguidores/seguir",
        json={"id_user_seguido": target.id_user},
        headers=headers,
    )

    assert resp.status_code == 400
    assert "Ya sigues a este usuario" in resp.json()["detail"]


def test_unfollow_ok(client: TestClient, test_db):
    """POST /api/v1/seguidores/unfollow elimina una relación existente."""
    current = create_test_user(test_db, "user_actual", "actual@example.com")
    target = create_test_user(test_db, "user_target", "target@example.com")

    rel = UsuarioSeguido(id_user=current.id_user, id_user_seguido=target.id_user)
    test_db.add(rel)
    test_db.commit()

    headers = create_auth_headers(current.username)
    resp = client.post(
        "/api/v1/seguidores/unfollow",
        json={"id_user_seguido": target.id_user},
        headers=headers,
    )

    assert resp.status_code == 200
    assert "Has dejado de seguir" in resp.json()["message"]

    rel_db = (
        test_db.query(UsuarioSeguido)
        .filter_by(id_user=current.id_user, id_user_seguido=target.id_user)
        .first()
    )
    assert rel_db is None


def test_unfollow_sin_seguir_previamente(client: TestClient, test_db):
    """No se puede dejar de seguir a alguien que no sigues (400)."""
    current = create_test_user(test_db, "user_actual", "actual@example.com")
    target = create_test_user(test_db, "user_target", "target@example.com")

    headers = create_auth_headers(current.username)
    resp = client.post(
        "/api/v1/seguidores/unfollow",
        json={"id_user_seguido": target.id_user},
        headers=headers,
    )

    assert resp.status_code == 400
    assert "No sigues a este usuario" in resp.json()["detail"]


def test_obtener_siguiendo(client: TestClient, test_db):
    """GET /api/v1/seguidores/siguiendo devuelve la lista de usuarios seguidos."""
    current = create_test_user(test_db, "user_actual", "actual@example.com")
    target1 = create_test_user(test_db, "user_target1", "t1@example.com")
    target2 = create_test_user(test_db, "user_target2", "t2@example.com")

    test_db.add(UsuarioSeguido(id_user=current.id_user, id_user_seguido=target1.id_user))
    test_db.add(UsuarioSeguido(id_user=current.id_user, id_user_seguido=target2.id_user))
    test_db.commit()

    headers = create_auth_headers(current.username)
    resp = client.get("/api/v1/seguidores/siguiendo", headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    usernames = {u["username"] for u in data}
    assert {target1.username, target2.username}.issubset(usernames)


def test_contar_seguidores(client: TestClient, test_db):
    """GET /api/v1/seguidores/count/{id_user} devuelve el número correcto."""
    owner = create_test_user(test_db, "owner", "owner@example.com")
    follower1 = create_test_user(test_db, "f1", "f1@example.com")
    follower2 = create_test_user(test_db, "f2", "f2@example.com")

    test_db.add(UsuarioSeguido(id_user=follower1.id_user, id_user_seguido=owner.id_user))
    test_db.add(UsuarioSeguido(id_user=follower2.id_user, id_user_seguido=owner.id_user))
    test_db.commit()

    resp = client.get(f"/api/v1/seguidores/count/{owner.id_user}")
    assert resp.status_code == 200
    assert resp.json()["seguidores"] == 2
