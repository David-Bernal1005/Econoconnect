from sqlalchemy.orm import Session
from ..models.chat import Chat
from ..models.user import User
from ..models.chatmiembro import ChatMiembro
from ..schemas.chat import ChatCreate
from ..core.security import get_current_user
from fastapi import HTTPException

def create_chat_group(db: Session, chat: ChatCreate, current_user: User):
    # Check if the user has permission to create this type of chat
    # Normalizar y aceptar varias formas ("administrador", "RoleEnum.administrador", etc.)
    if chat.visibilidad == "privado":
        rol_str = str(current_user.rol).lower()
        # debug log (se puede cambiar a logging)
        print(f"[chat_service] current_user.rol={rol_str}")
        if "administrador" not in rol_str:
            raise HTTPException(
                status_code=403,
                detail="Solo los administradores pueden crear grupos privados"
            )
    
    db_chat = Chat(
        nombre=chat.nombre,
        descripcion=chat.descripcion,
        tipo=chat.tipo,
        visibilidad=chat.visibilidad,
        creador_id=current_user.id_user,
        estado="activo"
    )
    
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_public_chats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Chat).filter(
        Chat.visibilidad == "publico",
        Chat.tipo == "grupo",
        Chat.estado == "activo"
    ).offset(skip).limit(limit).all()

def get_user_chats(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # Get all public chats and private chats where the user is a member
    return db.query(Chat).join(
        ChatMiembro,
        (Chat.id_chat == ChatMiembro.chat_id) & (ChatMiembro.user_id == user_id)
    ).union(
        db.query(Chat).filter(
            Chat.visibilidad == "publico",
            Chat.tipo == "grupo",
            Chat.estado == "activo"
        )
    ).offset(skip).limit(limit).all()