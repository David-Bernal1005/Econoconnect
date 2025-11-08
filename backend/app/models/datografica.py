from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from . import Base

class DatoGrafica(Base):
    __tablename__ = "dato_grafica"

    id_dato = Column(Integer, primary_key=True, autoincrement=True)
    id_grafica = Column(Integer, ForeignKey("grafica.id_grafica"))
    anio = Column(Integer)
    cop_usd = Column(DECIMAL(15, 2))
    cop_eur = Column(DECIMAL(15, 2))
    fecha_actualizacion = Column(Date)
    
    # Mantener compatibilidad con código existente
    etiqueta = Column(String(100))
    fecha = Column(Date)
    valor = Column(DECIMAL(15, 2))