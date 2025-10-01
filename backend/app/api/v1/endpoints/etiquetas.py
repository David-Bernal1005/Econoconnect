from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.etiqueta import Etiqueta
from app.db.session import get_db

router = APIRouter()

@router.get("/etiquetas", response_model=list)
def get_etiquetas(db: Session = Depends(get_db)):
    etiquetas = db.query(Etiqueta).all()
    # Devuelve solo los campos relevantes
    return [{
        "id_etiqueta": e.id_etiqueta,
        "nombre": e.nombre,
        "descripcion": e.descripcion,
        "autor_id": e.autor_id,
        "estado": e.estado,
        "fecha_creacion": str(e.fecha_creacion)
    } for e in etiquetas]
