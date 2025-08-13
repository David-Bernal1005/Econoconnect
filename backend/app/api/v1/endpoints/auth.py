from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

router  = APIRouter()

# Datos quemados de ejemplo (en producción usar DB)
fake_user = {"username": "admin@hotmail", "password": "1234"}

# Esquema de entrada
class LoginRequest(BaseModel):
    username: str
    password: str   

# Generar token JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

@router.post("/login")
def login(request: LoginRequest):
    if request.username != fake_user["username"] or request.password != fake_user["password"]:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({"sub": request.username})
    return {"access_token": token, "token_type": "bearer"}
