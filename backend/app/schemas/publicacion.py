from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ComentarioResponse(BaseModel):
    id_comentario: int
    texto: str
    fecha_comentario: datetime

    class Config:
        orm_mode = True

class PublicacionResponse(BaseModel):
    id_publicacion: int
    usuario_id: int
    titulo: str
    contenido: str
    fecha_creacion: datetime
    estado: str
    comentarios: Optional[List[ComentarioResponse]] = []

    class Config:
        orm_mode = True