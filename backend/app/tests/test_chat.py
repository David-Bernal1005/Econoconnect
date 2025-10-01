import pytest
from fastapi.testclient import TestClient
from app.models.chat import Chat
from app.models.chatmensaje import ChatMensaje
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


def test_get_user_chats_empty(client: TestClient, test_db):
    """Test getting user chats when user has no chats"""
    user = create_test_user(test_db)
    
    response = client.get(f"/api/v1/chats/{user.id_user}")
    assert response.status_code == 200
    assert response.json() == []


def test_get_user_chats_with_data(client: TestClient, test_db):
    """Test getting user chats with data"""
    user = create_test_user(test_db)
    
    # Create test chats
    chats = [
        Chat(
            nombre="Chat General",
            creador_id=user.id_user,
            fecha_creacion=datetime.now()
        ),
        Chat(
            nombre="Chat Tecnología",
            creador_id=user.id_user,
            fecha_creacion=datetime.now()
        ),
        Chat(
            nombre="Chat Economía",
            creador_id=user.id_user,
            fecha_creacion=datetime.now()
        )
    ]
    
    for chat in chats:
        test_db.add(chat)
    test_db.commit()
    test_db.refresh(chats[0])
    test_db.refresh(chats[1])
    test_db.refresh(chats[2])
    
    # Add messages to chats
    messages = [
        ChatMensaje(
            id_chat=chats[0].id_chat,
            id_user=user.id_user,
            contenido="Mensaje en chat general",
            fecha_envio=datetime.now()
        ),
        ChatMensaje(
            id_chat=chats[1].id_chat,
            id_user=user.id_user,
            contenido="Mensaje en chat tecnología",
            fecha_envio=datetime.now()
        )
    ]
    
    for message in messages:
        test_db.add(message)
    test_db.commit()
    
    response = client.get(f"/api/v1/chats/{user.id_user}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Verify chat structure
    for chat in data:
        assert "id_chat" in chat
        assert "nombre" in chat
        assert "ultimo_mensaje" in chat
        assert "fecha_ultimo" in chat
    
    # Verify chat names
    chat_names = [chat["nombre"] for chat in data]
    assert "Chat General" in chat_names
    assert "Chat Tecnología" in chat_names
    assert "Chat Economía" in chat_names


def test_get_user_chats_with_messages(client: TestClient, test_db):
    """Test getting user chats with last messages"""
    user = create_test_user(test_db)
    
    # Create chat
    chat = Chat(
        nombre="Test Chat",
        creador_id=user.id_user,
        fecha_creacion=datetime.now()
    )
    test_db.add(chat)
    test_db.commit()
    test_db.refresh(chat)
    
    # Add multiple messages (last one should be returned)
    messages = [
        ChatMensaje(
            id_chat=chat.id_chat,
            id_user=user.id_user,
            contenido="Primer mensaje",
            fecha_envio=datetime(2024, 1, 1, 10, 0, 0)
        ),
        ChatMensaje(
            id_chat=chat.id_chat,
            id_user=user.id_user,
            contenido="Segundo mensaje",
            fecha_envio=datetime(2024, 1, 1, 11, 0, 0)
        ),
        ChatMensaje(
            id_chat=chat.id_chat,
            id_user=user.id_user,
            contenido="Último mensaje",
            fecha_envio=datetime(2024, 1, 1, 12, 0, 0)
        )
    ]
    
    for message in messages:
        test_db.add(message)
    test_db.commit()
    
    response = client.get(f"/api/v1/chats/{user.id_user}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    
    chat_data = data[0]
    assert chat_data["id_chat"] == chat.id_chat
    assert chat_data["nombre"] == "Test Chat"
    assert chat_data["ultimo_mensaje"] == "Último mensaje"
    assert chat_data["fecha_ultimo"] is not None


def test_get_user_chats_no_messages(client: TestClient, test_db):
    """Test getting user chats with no messages"""
    user = create_test_user(test_db)
    
    # Create chat without messages
    chat = Chat(
        nombre="Empty Chat",
        creador_id=user.id_user,
        fecha_creacion=datetime.now()
    )
    test_db.add(chat)
    test_db.commit()
    test_db.refresh(chat)
    
    response = client.get(f"/api/v1/chats/{user.id_user}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    
    chat_data = data[0]
    assert chat_data["id_chat"] == chat.id_chat
    assert chat_data["nombre"] == "Empty Chat"
    assert chat_data["ultimo_mensaje"] == ""
    assert chat_data["fecha_ultimo"] is None


def test_get_user_chats_different_user(client: TestClient, test_db):
    """Test getting chats for different users"""
    user1 = create_test_user(test_db)
    
    # Create another user
    user2 = User(
        name="Maria",
        lastname="González",
        cellphone="+1234567891",
        direction="Calle 456",
        username="maria_gonzalez",
        hashed_password="hashed_password",
        rol="usuario",
        country="Colombia",
        email="maria@example.com",
        state=StateUser.activo,
        number_followers=0
    )
    test_db.add(user2)
    test_db.commit()
    test_db.refresh(user2)
    
    # Create chats for different users
    chat1 = Chat(
        nombre="Chat User 1",
        creador_id=user1.id_user,
        fecha_creacion=datetime.now()
    )
    chat2 = Chat(
        nombre="Chat User 2",
        creador_id=user2.id_user,
        fecha_creacion=datetime.now()
    )
    test_db.add(chat1)
    test_db.add(chat2)
    test_db.commit()
    
    # Test user1 chats
    response1 = client.get(f"/api/v1/chats/{user1.id_user}")
    assert response1.status_code == 200
    data1 = response1.json()
    assert len(data1) == 1
    assert data1[0]["nombre"] == "Chat User 1"
    
    # Test user2 chats
    response2 = client.get(f"/api/v1/chats/{user2.id_user}")
    assert response2.status_code == 200
    data2 = response2.json()
    assert len(data2) == 1
    assert data2[0]["nombre"] == "Chat User 2"


def test_get_user_chats_nonexistent_user(client: TestClient, test_db):
    """Test getting chats for non-existent user"""
    response = client.get("/api/v1/chats/999")
    assert response.status_code == 200
    assert response.json() == []