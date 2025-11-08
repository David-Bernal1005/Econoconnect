from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...db.session import get_db
from ...schemas.chat import ChatCreate, ChatResponse
from ...services.chat_service import create_chat_group, get_public_chats, get_user_chats
from ...core.security import get_current_user
from ...models.user import User

router = APIRouter()

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
    return create_chat_group(db=db, chat=chat, current_user=current_user)

@router.get("/grupos/publicos/", response_model=List[ChatResponse])
def list_public_groups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Listar todos los grupos públicos disponibles
    """
    return get_public_chats(db, skip=skip, limit=limit)

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
    return get_user_chats(db, user_id=current_user.id_user, skip=skip, limit=limit)