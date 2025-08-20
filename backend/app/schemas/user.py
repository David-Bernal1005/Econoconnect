from pydantic import BaseModel
from backend.app.api.v1.endpoints.auth import RoleEnum

class UserCreate(BaseModel):
    name: str
    lastname: str
    cellphone: int
    direction: str
    username: str
    password: str
    rol: RoleEnum

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    name: str
    lastname: str
    cellphone: int
    direction: str
    username: str
    rol: RoleEnum

    class Config:
        orm_mode = True
