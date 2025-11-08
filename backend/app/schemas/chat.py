from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo: str = "grupo"
    visibilidad: str = "privado"

class ChatCreate(ChatBase):
    pass

class ChatResponse(ChatBase):
    id_chat: int
    creador_id: int
    estado: str
    fecha_creacion: datetime

    class Config:
        orm_mode = True