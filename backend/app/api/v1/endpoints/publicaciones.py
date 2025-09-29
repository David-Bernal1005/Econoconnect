from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.publicacion import Publicacion

router = APIRouter()

@router.get("/publicaciones", response_model=list)
def get_publicaciones(db: Session = Depends(get_db)):
    return db.query(Publicacion).all()

