from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import models

router = APIRouter()

@router.get("/graficas")
def get_graficas(db: Session = Depends(get_db)):
    """
    Retorna datos de ejemplo para las gráficas.
    Puedes adaptar esto a tu modelo real (Grafica, DatoGrafica).
    """
    data = db.query(models.datografica.DatoGrafica).all()
    return [
        {"name": d.nombre, "value": d.valor}
        for d in data
    ]
