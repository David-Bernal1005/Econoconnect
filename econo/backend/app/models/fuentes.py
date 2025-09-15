from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from backend.app.db.session import Base
import enum

class Fuente(Base):
    __tablename__ = "fuentes"

    Id_Fuente = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_Fuente = Column(String(100))
    Url_Fuente = Column(String(500))
    Tipo_Fuente = Column(String(50))
