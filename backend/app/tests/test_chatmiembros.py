import pytest
from fastapi.testclient import TestClient
from app.models.user import User, StateUser
from app.models.chat import Chat
from app.models.chatmiembro import ChatMiembro
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


def create_chat(test_db, creador_id: int, visibilidad: str = "publico") -> Chat:
    chat = Chat(
        nombre="Chat Test",
        descripcion="desc",
        tipo="grupo",
        visibilidad=visibilidad,
        creador_id=creador_id,
        estado="activo",
    )
    test_db.add(chat)
    test_db.commit()
    test_db.refresh(chat)
    return chat


def test_agregar_miembro_public_chat_sin_admin(client: TestClient, test_db):
    """En chats públicos se permite agregar miembros aunque el actual no sea admin."""
    owner = create_test_user(test_db, "owner", "owner@example.com")
    nuevo = create_test_user(test_db, "nuevo", "nuevo@example.com")
    chat = create_chat(test_db, creador_id=owner.id_user, visibilidad="publico")

    headers = create_auth_headers(owner.username)
    resp = client.post(
        f"/api/v1/chats/{chat.id_chat}/miembros/",
        json={"id_user": nuevo.id_user, "rol_chat": "miembro"},
        headers=headers,
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["id_chat"] == chat.id_chat
    assert body["id_user"] == nuevo.id_user
    assert body["rol_chat"] == "miembro"


def test_agregar_miembro_chat_privado_sin_permisos(client: TestClient, test_db):
    """En chat privado, un usuario sin rol admin no puede agregar miembros."""
    owner = create_test_user(test_db, "owner", "owner@example.com")
    nuevo = create_test_user(test_db, "nuevo", "nuevo@example.com")
    chat = create_chat(test_db, creador_id=owner.id_user, visibilidad="privado")

    headers = create_auth_headers(owner.username)
    resp = client.post(
        f"/api/v1/chats/{chat.id_chat}/miembros/",
        json={"id_user": nuevo.id_user, "rol_chat": "miembro"},
        headers=headers,
    )

    assert resp.status_code == 403
    assert "No tienes permisos" in resp.json()["detail"]


def test_agregar_miembro_chat_privado_como_admin(client: TestClient, test_db):
    """Un admin del chat privado sí puede agregar miembros."""
    owner = create_test_user(test_db, "owner", "owner@example.com")
    nuevo = create_test_user(test_db, "nuevo", "nuevo@example.com")
    chat = create_chat(test_db, creador_id=owner.id_user, visibilidad="privado")

    # Hacer al owner admin del chat
    admin = ChatMiembro(id_chat=chat.id_chat, id_user=owner.id_user, rol_chat="admin")
    test_db.add(admin)
    test_db.commit()

    headers = create_auth_headers(owner.username)
    resp = client.post(
        f"/api/v1/chats/{chat.id_chat}/miembros/",
        json={"id_user": nuevo.id_user, "rol_chat": "miembro"},
        headers=headers,
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["id_user"] == nuevo.id_user


def test_obtener_miembros_chat_privado_sin_ser_miembro(client: TestClient, test_db):
    """No se puede ver miembros de un chat privado si no eres miembro."""
    owner = create_test_user(test_db, "owner", "owner@example.com")
    externo = create_test_user(test_db, "externo", "externo@example.com")
    chat = create_chat(test_db, creador_id=owner.id_user, visibilidad="privado")

    # owner es miembro admin
    test_db.add(ChatMiembro(id_chat=chat.id_chat, id_user=owner.id_user, rol_chat="admin"))
    test_db.commit()

    headers = create_auth_headers(externo.username)
    resp = client.get(f"/api/v1/chats/{chat.id_chat}/miembros/", headers=headers)

    assert resp.status_code == 403
    assert "No tienes acceso" in resp.json()["detail"]


def test_obtener_miembros_chat_privado_como_miembro(client: TestClient, test_db):
    """Un miembro del chat privado puede listar miembros."""
    owner = create_test_user(test_db, "owner", "owner@example.com")
    miembro = create_test_user(test_db, "miembro", "miembro@example.com")
    chat = create_chat(test_db, creador_id=owner.id_user, visibilidad="privado")

    test_db.add(ChatMiembro(id_chat=chat.id_chat, id_user=owner.id_user, rol_chat="admin"))
    test_db.add(ChatMiembro(id_chat=chat.id_chat, id_user=miembro.id_user, rol_chat="miembro"))
    test_db.commit()

    headers = create_auth_headers(miembro.username)
    resp = client.get(f"/api/v1/chats/{chat.id_chat}/miembros/", headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    ids = {m["id_user"] for m in data}
    assert {owner.id_user, miembro.id_user}.issubset(ids)


def test_eliminar_miembro_por_admin(client: TestClient, test_db):
    """Un admin puede eliminar a otro miembro del chat."""
    owner = create_test_user(test_db, "owner", "owner@example.com")
    miembro = create_test_user(test_db, "miembro", "miembro@example.com")
    chat = create_chat(test_db, creador_id=owner.id_user, visibilidad="publico")

    test_db.add(ChatMiembro(id_chat=chat.id_chat, id_user=owner.id_user, rol_chat="admin"))
    test_db.add(ChatMiembro(id_chat=chat.id_chat, id_user=miembro.id_user, rol_chat="miembro"))
    test_db.commit()

    headers = create_auth_headers(owner.username)
    resp = client.delete(f"/api/v1/chats/{chat.id_chat}/miembros/{miembro.id_user}", headers=headers)

    assert resp.status_code == 200
    assert "Miembro eliminado" in resp.json()["message"]

    exists = (
        test_db.query(ChatMiembro)
        .filter_by(id_chat=chat.id_chat, id_user=miembro.id_user)
        .first()
    )
    assert exists is None


def test_eliminar_ultimo_admin_prohibido(client: TestClient, test_db):
    """No se puede eliminar al último admin del chat."""
    owner = create_test_user(test_db, "owner", "owner@example.com")
    chat = create_chat(test_db, creador_id=owner.id_user, visibilidad="publico")

    test_db.add(ChatMiembro(id_chat=chat.id_chat, id_user=owner.id_user, rol_chat="admin"))
    test_db.commit()

    headers = create_auth_headers(owner.username)
    resp = client.delete(f"/api/v1/chats/{chat.id_chat}/miembros/{owner.id_user}", headers=headers)

    assert resp.status_code == 400
    assert "No se puede eliminar al último administrador" in resp.json()["detail"]


def test_actualizar_rol_por_admin(client: TestClient, test_db):
    """Un admin puede cambiar el rol de otro miembro."""
    owner = create_test_user(test_db, "owner", "owner@example.com")
    miembro = create_test_user(test_db, "miembro", "miembro@example.com")
    chat = create_chat(test_db, creador_id=owner.id_user, visibilidad="publico")

    test_db.add(ChatMiembro(id_chat=chat.id_chat, id_user=owner.id_user, rol_chat="admin"))
    test_db.add(ChatMiembro(id_chat=chat.id_chat, id_user=miembro.id_user, rol_chat="miembro"))
    test_db.commit()

    headers = create_auth_headers(owner.username)
    resp = client.patch(
        f"/api/v1/chats/{chat.id_chat}/miembros/{miembro.id_user}/rol",
        json={"rol_chat": "admin"},
        headers=headers,
    )

    assert resp.status_code == 200
    assert resp.json()["rol_chat"] == "admin"


def test_actualizar_rol_sin_ser_admin(client: TestClient, test_db):
    """Un miembro sin rol admin no puede cambiar roles de otros."""
    owner = create_test_user(test_db, "owner", "owner@example.com")
    miembro = create_test_user(test_db, "miembro", "miembro@example.com")
    chat = create_chat(test_db, creador_id=owner.id_user, visibilidad="publico")

    test_db.add(ChatMiembro(id_chat=chat.id_chat, id_user=owner.id_user, rol_chat="miembro"))
    test_db.add(ChatMiembro(id_chat=chat.id_chat, id_user=miembro.id_user, rol_chat="miembro"))
    test_db.commit()

    headers = create_auth_headers(owner.username)
    resp = client.patch(
        f"/api/v1/chats/{chat.id_chat}/miembros/{miembro.id_user}/rol",
        json={"rol_chat": "admin"},
        headers=headers,
    )

    assert resp.status_code == 403
    assert "Solo los administradores" in resp.json()["detail"]
