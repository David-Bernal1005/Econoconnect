from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoticiaSchema(BaseModel):
    Id_Noticia: Optional[int] = None
    titulo: str
    resumen: str
    enlace: str
    fecha_publicacion: datetime
    Id_Categoria: Optional[int] = None
    Id_Fuente: Optional[int] = None
    usuario: Optional[str] = None
    activa: Optional[int] = 1
    profile_image: Optional[str] = None
    etiquetas: Optional[list[str]] = []

    model_config = {
        "from_attributes": True
    }

class NoticiaStatusResponse(BaseModel):
    Id_Noticia: int
    titulo: str
    activa: int
    mensaje: str = "Operación exitosa"

    model_config = {
        "from_attributes": True
    }
