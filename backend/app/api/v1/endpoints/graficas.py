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
    Usa múltiples fuentes de datos y guarda en DB para backup.
    """
    try:
        # 1. Intentar obtener datos actuales
        current_year = datetime.date.today().year
        if end_year is None:
            end_year = current_year

        # 2. Obtener datos históricos de la DB (filtrando por id_grafica)
        # traer todos los registros para esa grafica y derivar el año si hace falta
        historical_data = db.query(models.datografica.DatoGrafica).filter(
            models.datografica.DatoGrafica.id_grafica == grafica_id,
        ).all()

        # 3. Convertir a diccionario para fácil acceso
        data_by_year = {}
        for d in historical_data:
            # Intentar obtener año desde la columna 'anio', si no, desde 'fecha' o 'fecha_actualizacion'
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

            # Si no hay año, intentar inferirlo de 'valor' u otra columna (no ideal)
            if year_key is None:
                # fallback: usar el año actual si no hay otro dato
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

            # Guardar/mezclar valores (si hay múltiples registros por año, conservamos el último)
            data_by_year[year_key] = {
                'cop_usd': cop_usd,
                'cop_eur': cop_eur,
                'fecha_actualizacion': getattr(d, 'fecha_actualizacion', None)
            }

        # 4. Obtener tasas actuales
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
            
            # Actualizar datos del año actual
            data_by_year[current_year] = current_rates

        # 5. Construir respuesta usando todos los años disponibles para la grafica
        result = []
        years = sorted(set(list(data_by_year.keys())))
        # Si el usuario pidió un rango mayor, también incluir esos años if present
        for year in years:
            if year >= start_year and year <= end_year:
                result.append({
                    "year": str(year),
                    "cop_usd": data_by_year[year].get("cop_usd"),
                    "cop_eur": data_by_year[year].get("cop_eur")
                })

        return result

    except Exception as e:
        logger.error(f"Error en get_graficas: {e}")
        # Si hay error, intentar devolver solo datos históricos de la DB
        try:
            data = db.query(models.datografica.DatoGrafica).all()
            if data:
                return sorted([{
                    "year": str(d.anio),
                    "cop_usd": float(d.cop_usd) if d.cop_usd else None,
                    "cop_eur": float(d.cop_eur) if d.cop_eur else None
                } for d in data], key=lambda x: x["year"])
        except Exception as db_error:
            logger.error(f"Error obteniendo datos de respaldo: {db_error}")
        
        raise HTTPException(
            status_code=500,
            detail="No se pudieron obtener datos de tasas de cambio"
        )