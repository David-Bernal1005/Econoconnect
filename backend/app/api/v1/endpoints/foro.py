from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.foro import Foro, EstadoForo
from app.models.user import User
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import JWTError, jwt
from app.core.config import settings

router = APIRouter(prefix="/foro", tags=["Foro"])
security = HTTPBearer()

class ForoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    id_grafica: Optional[int] = None

class ForoCreate(ForoBase):
    pass

class ForoResponse(ForoBase):
    id_foro: int
    autor_id: int
    estado: EstadoForo
    fecha_creacion: datetime
    autor_username: str

    class Config:
        from_attributes = True

def get_user_from_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if not username:
            return None
    except JWTError:
        return None
    user = db.query(User).filter(User.username == username).first()
    return user

@router.post("", response_model=ForoResponse)
async def crear_foro(
    foro: ForoCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    user = get_user_from_token(credentials.credentials, db)
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")

    db_foro = Foro(
        nombre=foro.nombre,
        descripcion=foro.descripcion,
        autor_id=user.id_user,
        id_grafica=foro.id_grafica,
        estado=EstadoForo.activo
    )
    db.add(db_foro)
    db.commit()
    db.refresh(db_foro)
    
    return ForoResponse(
        **db_foro.__dict__,
        autor_username=user.username
    )

@router.get("", response_model=List[ForoResponse])
async def listar_foros(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    user = get_user_from_token(credentials.credentials, db)
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")

    foros = db.query(Foro).filter(Foro.estado == EstadoForo.activo).all()
    return [
        ForoResponse(
            **foro.__dict__,
            autor_username=foro.autor.username if foro.autor else None
        ) 
        for foro in foros
    ]

@router.get("/{foro_id}", response_model=ForoResponse)
async def obtener_foro(
    foro_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    user = get_user_from_token(credentials.credentials, db)
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")

    foro = db.query(Foro).filter(Foro.id_foro == foro_id, Foro.estado == EstadoForo.activo).first()
    if not foro:
        raise HTTPException(status_code=404, detail="Foro no encontrado")

    return ForoResponse(
        **foro.__dict__,
        autor_username=foro.autor.username if foro.autor else None
    )

@router.delete("/{foro_id}")
async def eliminar_foro(
    foro_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    user = get_user_from_token(credentials.credentials, db)
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")

    foro = db.query(Foro).filter(Foro.id_foro == foro_id).first()
    if not foro:
        raise HTTPException(status_code=404, detail="Foro no encontrado")
    
    if foro.autor_id != user.id_user:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este foro")

    foro.estado = EstadoForo.inactivo
    db.commit()
    
    return {"message": "Foro eliminado correctamente"}