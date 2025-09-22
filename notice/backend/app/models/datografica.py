from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from backend.app.db.session import Base

class DatoGrafica(Base):
    __tablename__ = "dato_grafica"

    id_dato = Column(Integer, primary_key=True, autoincrement=True)
    id_grafica = Column(Integer, ForeignKey("grafica.id_grafica"))
    etiqueta = Column(String(100))
    fecha = Column(Date)
    valor = Column(DECIMAL(15, 2))
