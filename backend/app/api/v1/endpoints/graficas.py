from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import models
import logging

import datetime
import httpx
from typing import List
import json
from decimal import Decimal

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def _save_to_db(db: Session, year: int, usd_rate: float, eur_rate: float, grafica_id: int = 1):
    """Guarda o actualiza tasas en la base de datos"""
    try:
        dato = db.query(models.datografica.DatoGrafica).filter(
            models.datografica.DatoGrafica.anio == year,
            models.datografica.DatoGrafica.id_grafica == grafica_id,
        ).first()
        
        if dato:
            dato.cop_usd = usd_rate
            dato.cop_eur = eur_rate
            dato.fecha_actualizacion = datetime.date.today()
        else:
            dato = models.datografica.DatoGrafica(
                id_grafica=grafica_id,
                anio=year,
                cop_usd=usd_rate,
                cop_eur=eur_rate,
                fecha_actualizacion=datetime.date.today()
            )
            db.add(dato)
        
        db.commit()
        logger.info(f"Datos guardados para el año {year}")
    except Exception as e:
        logger.error(f"Error guardando datos: {e}")
        db.rollback()

def _get_exchange_rates(currency: str) -> dict:
    """Obtiene tasas de cambio desde APIs públicas"""
    apis = [
        f"https://api.exchangerate-api.com/v4/latest/{currency}",
        f"https://open.er-api.com/v6/latest/{currency}",
        f"https://api.exchangerate.host/latest?base={currency}&symbols=COP"
    ]
    
    for api_url in apis:
        try:
            with httpx.Client(timeout=10.0) as client:
                resp = client.get(api_url)
                if resp.status_code == 200:
                    data = resp.json()
                    if "rates" in data and "COP" in data["rates"]:
                        return {"success": True, "rate": data["rates"]["COP"]}
            logger.warning(f"API {api_url} no devolvió datos para COP")
        except Exception as e:
            logger.error(f"Error consultando {api_url}: {e}")
    
    return {"success": False, "error": "No se pudo obtener la tasa de cambio"}

@router.get("/graficas")
async def get_graficas(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    start_year: int = Query(2018, ge=1999),
    end_year: int | None = None,
    grafica_id: int = Query(1, ge=1),
):
    """
    Retorna datos para las gráficas comparando USD y EUR frente al COP.
    Si no se pueden obtener datos actuales, devuelve los datos históricos de la base de datos.
    """
    current_year = datetime.date.today().year
    if end_year is None:
        end_year = current_year

    # Obtener datos históricos de la DB (filtrando por id_grafica)
    historical_data = db.query(models.datografica.DatoGrafica).filter(
        models.datografica.DatoGrafica.id_grafica == grafica_id,
    ).all()

    # Convertir a diccionario para fácil acceso
    data_by_year = {}
    for d in historical_data:
        year_key = None
        try:
            if getattr(d, 'anio', None):
                year_key = int(d.anio)
            elif getattr(d, 'fecha', None):
                year_key = int(d.fecha.year)
            elif getattr(d, 'fecha_actualizacion', None):
                year_key = int(d.fecha_actualizacion.year)
        except Exception:
            year_key = None
        if year_key is None:
            year_key = datetime.date.today().year
        cop_usd = None
        cop_eur = None
        try:
            if getattr(d, 'cop_usd', None) is not None:
                cop_usd = float(d.cop_usd)
            elif getattr(d, 'valor', None) is not None:
                cop_usd = float(d.valor)
        except Exception:
            cop_usd = None
        try:
            if getattr(d, 'cop_eur', None) is not None:
                cop_eur = float(d.cop_eur)
            elif getattr(d, 'valor', None) is not None:
                cop_eur = float(d.valor)
        except Exception:
            cop_eur = None
        data_by_year[year_key] = {
            'cop_usd': cop_usd,
            'cop_eur': cop_eur,
            'fecha_actualizacion': getattr(d, 'fecha_actualizacion', None)
        }

    # Intentar obtener tasas actuales
    try:
        usd_data = _get_exchange_rates("USD")
        eur_data = _get_exchange_rates("EUR")
        if usd_data["success"] and eur_data["success"]:
            current_rates = {
                "cop_usd": round(usd_data["rate"], 2),
                "cop_eur": round(eur_data["rate"], 2)
            }
            # Guardar tasas actuales en DB (async)
            background_tasks.add_task(
                _save_to_db,
                db=db,
                year=current_year,
                usd_rate=current_rates["cop_usd"],
                eur_rate=current_rates["cop_eur"],
                grafica_id=grafica_id,
            )
            data_by_year[current_year] = current_rates
    except Exception as e:
        logger.error(f"Error obteniendo tasas actuales: {e}")

    # Construir respuesta usando todos los años disponibles para la grafica
    result = []
    years = sorted(set(list(data_by_year.keys())))
    for year in years:
        if year >= start_year and year <= end_year:
            result.append({
                "year": str(year),
                "cop_usd": data_by_year[year].get("cop_usd"),
                "cop_eur": data_by_year[year].get("cop_eur")
            })

    if result:
        return result
    else:
        return {"message": "No hay datos históricos en la base de datos para esta gráfica."}