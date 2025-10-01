from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.user import StateUser
from enum import Enum

class RoleEnum(str, Enum):
    administrador = "administrador"
    usuario = "usuario"

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
    rol: RoleEnum
    email: EmailStr | None = None 
    state: StateUser
    creation_date: datetime
    last_activity_date: datetime 
    number_followers: int
    profile_image: str | None = None
class UserUpdateRequest(BaseModel):
    name: str
    lastname: str
    email: str
    cellphone: str
    direction: str
    country: str
    profile_image: str | None = None

    model_config = {
        "from_attributes": True
    }
