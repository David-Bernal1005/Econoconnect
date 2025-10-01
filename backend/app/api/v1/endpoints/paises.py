from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.paises import Pais
from pydantic import BaseModel
from typing import List

router = APIRouter()

class PaisSchema(BaseModel):
    id_pais: int
    nombre: str
    codigo_iso: str | None = None
    codigo_telefono: str | None = None

    model_config = {
        "from_attributes": True
    }

@router.get("/paises", response_model=List[PaisSchema])
def get_paises(db: Session = Depends(get_db)):
    """Obtener todos los países"""
    paises = db.query(Pais).order_by(Pais.nombre).all()
    return paises

@router.post("/paises", response_model=PaisSchema)
def create_pais(pais_data: dict, db: Session = Depends(get_db)):
    """Crear un nuevo país"""
    pais = Pais(**pais_data)
    db.add(pais)
    db.commit()
    db.refresh(pais)
    return pais