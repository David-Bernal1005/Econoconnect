from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MiembroBase(BaseModel):
    id_user: int
    rol_chat: str = "miembro"

class MiembroCreate(MiembroBase):
    pass

class MiembroUpdate(BaseModel):
    rol_chat: str

class MiembroResponse(MiembroBase):
    id_chat: int
    fecha_ingreso: datetime

    class Config:
        orm_mode = True

class MiembroInvitation(BaseModel):
    usuarios: List[int]  # Lista de IDs de usuarios a invitar