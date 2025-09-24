from datetime import datetime
from pydantic import BaseModel, EmailStr, constr, Field
from app.models.user import StateUser
from enum import Enum

class RoleEnum(str, Enum):
    administrador = "administrador"
    usuario = "usuario"

class RegisterRequest(BaseModel):
    name: str
    lastname: str
    cellphone: str
    direction: str
    username: str
    password: str
    country: str
    rol: RoleEnum
    email: EmailStr | None = None
    state: StateUser = StateUser.activo

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id_user: int
    name: str
    lastname: str
    cellphone: str
    direction: str
    username: str
    country: str
    rol: RoleEnum
    email: EmailStr | None = None 
    state: StateUser
    creation_date: datetime
    last_activity_date: datetime 
    number_followers: int

    class Config:
        orm_mode = True
