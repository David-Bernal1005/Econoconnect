from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.user import StateUser
from enum import Enum
from typing import Optional

class RoleEnum(str, Enum):
    administrador = "administrador"
    usuario = "usuario"

class PaisResponse(BaseModel):
    id_pais: int
    nombre: str
    codigo_iso: str
    codigo_telefono: str | None = None
    
    model_config = {
        "from_attributes": True
    }

class RegisterRequest(BaseModel):
    name: str
    lastname: str
    cellphone: str | None = None
    direction: str | None = None
    username: str
    password: str
    country: str | None = None
    rol: RoleEnum = RoleEnum.usuario
    email: EmailStr | None = None
    state: StateUser = StateUser.activo

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id_user: int
    name: str
    lastname: str
    cellphone: str | None = None
    direction: str | None = None
    username: str
    country: str | None = None
    id_pais: int | None = None  # Nuevo campo para la relación con países
    rol: RoleEnum
    email: EmailStr | None = None
    state: StateUser
    creation_date: datetime
    last_activity_date: datetime | None = None
    number_followers: int
    profile_image: str | None = None
    pais: Optional[PaisResponse] = None  # Información del país relacionado

    model_config = {
        "from_attributes": True
    }
class UserUpdateRequest(BaseModel):
    name: str
    lastname: str
    email: str
    cellphone: str
    direction: str
    country: str
    id_pais: int | None = None  # Nuevo campo para la relación con países
    profile_image: str | None = None

    model_config = {
        "from_attributes": True
    }
