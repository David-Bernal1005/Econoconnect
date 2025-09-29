from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.chat import Chat
from app.models.chatmensaje import ChatMensaje

router = APIRouter()

@router.get("/chats/{user_id}")
def get_user_chats(user_id: int, db: Session = Depends(get_db)):
    
    chats = db.query(Chat).filter(Chat.creador_id == user_id).all()
    
    result = []
    for chat in chats:
        last_msg = {
            db.query(ChatMensaje)
            .filter(ChatMensaje.id_chat == chat.id_chat)
            .order_by(ChatMensaje.fecha_envio.desc())
            .first()
        }
        result.append({
            "id_chat": chat.id_chat,
            "nombre": chat.nombre,
            "ultimo_mensaje": last_msg.contenido if last_msg else "",
            "fecha_ultimo": str(last_msg.fecha_envio) if last_msg else None,
        })
    return result 