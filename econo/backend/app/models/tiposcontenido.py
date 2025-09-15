from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from backend.app.db.session import Base
import enum

class TipoContenido(Base):
    __tablename__ = "tipos_contenido"

    Id_Tipo = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_Tipo = Column(String(50))
    Descripcion = Column(Text)
