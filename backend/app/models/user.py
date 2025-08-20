from pydantic import BaseModel, EmailStr
from enum import Enum

class RoleEnum(str, Enum):
    administrador = "administrador"
    usuario = "usuario"

class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    rol: RoleEnum
