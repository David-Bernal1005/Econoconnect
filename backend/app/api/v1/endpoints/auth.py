from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
from werkzeug.security import check_password_hash
from app.core.config import settings
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_user_by_username
from enum import Enum

router  = APIRouter()


fake_user = {"username": "admin@hotmail", "password": "1234"}

# Esquema de entrada del Login
class LoginRequest(BaseModel):
    username: str
    password: str  

#tipo de rol 
class RoleEnum(str, Enum):
    administrador = "administrador"
    usuario = "usuario" 

#Esquema de para datos del register
class RegisterRequest(BaseModel):
    name: str
    lastname: str
    cellphone: int
    direction: str
    username: str
    password: str
    rol: RoleEnum

# Generar token JWT para Login
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

@router.post("/login")
def login(request: LoginRequest):
    # Buscar el usuario en Mongo
    user = get_user_by_username(request.username)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Verificar contraseña
    if not check_password_hash(user["password"], request.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Generar token JWT
    token = create_access_token({"sub": request.username, "rol": user["rol"]})
    return {"access_token": token, "token_type": "bearer"}

#api para el Register
@router.post("/register", response_model=UserResponse)
async def register(user: RegisterRequest):
    existing_user = None  # Aquí deberías hacer consulta a la DB
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario ya existente")

    # Crea el usuario en la base de datos (ejemplo con servicio)
    new_user = create_user(user.name, user.lastname, user.cellphone, user.direction, user.username, user.password, user.rol)
    return new_user
