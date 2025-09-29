from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from . import Base
import enum

class Adjunto(Base):
    __tablename__ = "adjunto"

    id_adjunto = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(50))
    url = Column(String(500))
    autor_id = Column(Integer, ForeignKey("users.id_user"))
    estado = Column(Enum("activo", "eliminado", name="estado_adjunto"), default="activo")
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
