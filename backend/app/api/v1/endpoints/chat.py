from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.chat import Chat
from app.models.chatmensaje import ChatMensaje
from app.models.chatmiembro import ChatMiembro
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.chat import ChatCreate, ChatResponse

router = APIRouter()

@router.get("/chats/{user_id}")
def get_user_chats(user_id: int, db: Session = Depends(get_db)):
    chats = db.query(Chat).filter(Chat.creador_id == user_id).all()
    
    result = []
    for chat in chats:
        last_msg = db.query(ChatMensaje).filter(ChatMensaje.id_chat == chat.id_chat).order_by(ChatMensaje.fecha_envio.desc()).first()
        result.append({
            "id_chat": chat.id_chat,
            "nombre": chat.nombre,
            "tipo": chat.tipo,
            "visibilidad": chat.visibilidad,
            "ultimo_mensaje": last_msg.contenido if last_msg else "",
            "fecha_ultimo": str(last_msg.fecha_envio) if last_msg else None,
        })
    return result

@router.post("/grupos/", response_model=ChatResponse)
def create_group(
    chat: ChatCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo grupo de chat.
    Solo los administradores pueden crear grupos privados.
    Usuarios normales pueden crear grupos públicos.
    """
    # Verificar si el usuario tiene permisos para crear grupos privados
    if chat.visibilidad == "privado" and str(current_user.rol) != "administrador":
        raise HTTPException(
            status_code=403,
            detail="Solo los administradores pueden crear grupos privados"
        )
    
    db_chat = Chat(
        nombre=chat.nombre,
        descripcion=chat.descripcion,
        tipo="grupo",
        visibilidad=chat.visibilidad,
        creador_id=current_user.id_user,
        estado="activo"
    )
    
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    
    # Agregar al creador como miembro del grupo (usar nombres de columnas correctos)
    miembro = ChatMiembro(
        id_chat=db_chat.id_chat,
        id_user=current_user.id_user,
        rol_chat="admin"
    )
    db.add(miembro)
    db.commit()
    
    return db_chat

@router.get("/grupos/publicos/", response_model=List[ChatResponse])
def list_public_groups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Listar todos los grupos públicos disponibles
    """
    return db.query(Chat).filter(
        Chat.visibilidad == "publico",
        Chat.tipo == "grupo",
        Chat.estado == "activo"
    ).offset(skip).limit(limit).all()

@router.get("/grupos/mis-grupos/", response_model=List[ChatResponse])
def list_user_groups(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Listar todos los grupos del usuario (públicos y privados donde es miembro)
    """
    # Obtener todos los chats públicos y privados donde el usuario es miembro
    return db.query(Chat).join(
        ChatMiembro,
        (Chat.id_chat == ChatMiembro.chat_id) & (ChatMiembro.user_id == current_user.id_user)
    ).union(
        db.query(Chat).filter(
            Chat.visibilidad == "publico",
            Chat.tipo == "grupo",
            Chat.estado == "activo"
        )
    ).offset(skip).limit(limit).all()