from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.chat import ChatCreate, ChatResponse
from app.services.chat_service import crear_chat, listar_chats_usuario, obtener_chat, cambiar_estado_chat

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def crear(chat: ChatCreate, db: Session = Depends(get_db)):
    return crear_chat(db, chat)

@router.get("/usuario/{id_user}", response_model=List[ChatResponse])
def listar_chats(id_user: int, db: Session = Depends(get_db)):
    return listar_chats_usuario(db, id_user)

@router.get("/{id_chat}", response_model=ChatResponse)
def obtener(id_chat: int, db: Session = Depends(get_db)):
    return obtener_chat(db, id_chat)

@router.put("/{id_chat}/estado", response_model=ChatResponse)
def cambiar_estado(id_chat: int, nuevo_estado: str, db: Session = Depends(get_db)):
    return cambiar_estado_chat(db, id_chat, nuevo_estado)
