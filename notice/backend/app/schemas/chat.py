from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

class ChatBase(BaseModel):
    nombre: str
    tipo: Literal["privado", "grupo"] = "privado"
    descripcion: Optional[str] = None

class ChatCreate(ChatBase):
    creador_id: int

class ChatResponse(ChatBase):
    id_chat: int
    estado: Literal["activo", "inactivo"]
    fecha_creacion: datetime

    class Config:
        orm_mode = True