from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.models.usuarioseguido import UsuarioSeguido
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/seguidores", tags=["seguidores"])

# 📦 Modelo para solicitudes
class SeguirRequest(BaseModel):
    id_user_seguido: int


# 📋 Obtener sugerencias de usuarios
@router.get("/sugerencias")
def sugerencias(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    usuarios = (
        db.query(User)
        .filter(User.id_user != current_user.id_user)
        .limit(5)
        .all()
    )
    return usuarios


# ❤️ Seguir usuario
@router.post("/seguir")
def seguir_usuario(
    data: SeguirRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    id_user_seguido = data.id_user_seguido

    if id_user_seguido == current_user.id_user:
        raise HTTPException(status_code=400, detail="No puedes seguirte a ti mismo")

    ya_sigue = (
        db.query(UsuarioSeguido)
        .filter_by(id_user=current_user.id_user, id_user_seguido=id_user_seguido)
        .first()
    )

    if ya_sigue:
        raise HTTPException(status_code=400, detail="Ya sigues a este usuario")

    nuevo = UsuarioSeguido(
        id_user=current_user.id_user,
        id_user_seguido=id_user_seguido
    )
    db.add(nuevo)
    db.commit()
    return {"message": "Usuario seguido correctamente"}


# 💔 Dejar de seguir
@router.post("/unfollow")
def dejar_de_seguir(
    data: SeguirRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    id_user_seguido = data.id_user_seguido

    relacion = (
        db.query(UsuarioSeguido)
        .filter_by(id_user=current_user.id_user, id_user_seguido=id_user_seguido)
        .first()
    )

    if not relacion:
        raise HTTPException(status_code=400, detail="No sigues a este usuario")

    db.delete(relacion)
    db.commit()
    return {"message": "Has dejado de seguir al usuario"}


# 👀 Ver a quién sigo
@router.get("/siguiendo")
def obtener_siguiendo(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    siguiendo = (
        db.query(User)
        .join(UsuarioSeguido, UsuarioSeguido.id_user_seguido == User.id_user)
        .filter(UsuarioSeguido.id_user == current_user.id_user)
        .all()
    )
    return siguiendo

# 👥 Contar seguidores
@router.get("/count/{id_user}")
def contar_seguidores(id_user: int, db: Session = Depends(get_db)):
    count = db.query(UsuarioSeguido).filter(UsuarioSeguido.id_user_seguido == id_user).count()
    return {"seguidores": count}
