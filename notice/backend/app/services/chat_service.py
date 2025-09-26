from sqlalchemy.orm import Session
from app.models.chat import Chat
from app.schemas.chat import ChatCreate

def crear_chat(db: Session, chat: ChatCreate):
    db_chat = Chat(**chat.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def listar_chats_usuario(db: Session, id_user: int):
    # Opción básica: filtrar por creador
    return db.query(Chat).filter(Chat.creador_id == id_user).all()

def obtener_chat(db: Session, id_chat: int):
    return db.query(Chat).filter(Chat.id_chat == id_chat).first()

def cambiar_estado_chat(db: Session, id_chat: int, nuevo_estado: str):
    chat = db.query(Chat).filter(Chat.id_chat == id_chat).first()
    if chat:
        chat.estado = nuevo_estado
        db.commit()
        db.refresh(chat)
    return chat