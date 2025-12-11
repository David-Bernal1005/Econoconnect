from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.publicacion import Publicacion
from typing import List


class PublicacionSchemaOut:
    """Esquema de salida ligero para publicaciones.

    Se usa un schema simple basado en dict para evitar problemas de
    serialización directa del modelo SQLAlchemy.
    """

    @staticmethod
    def from_model(p: Publicacion) -> dict:
        return {
            "id_publicacion": p.id_publicacion,
            "id_user": p.id_user,
            "foro_id": p.foro_id,
            "titulo": p.titulo,
            "contenido": p.contenido,
            "estado": p.estado,
            "fecha_creacion": str(p.fecha_creacion) if p.fecha_creacion else None,
            "cantidad_comentarios": p.cantidad_comentarios,
            "slug": p.slug,
            "fecha_ultima_actividad": str(p.fecha_ultima_actividad) if p.fecha_ultima_actividad else None,
        }

router = APIRouter()


@router.get("/publicaciones")
def get_publicaciones(db: Session = Depends(get_db)):
    """Devuelve todas las publicaciones en formato JSON serializable."""
    publicaciones: List[Publicacion] = db.query(Publicacion).all()
    return [PublicacionSchemaOut.from_model(p) for p in publicaciones]

