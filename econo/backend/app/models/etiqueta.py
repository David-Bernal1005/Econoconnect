from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from backend.app.db.session import Base
import enum

class Etiqueta(Base):
    __tablename__ = "etiqueta"

    id_etiqueta = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    descripcion = Column(String(450))
    autor_id = Column(Integer, ForeignKey("users.id_user"))
    estado = Column(Enum("activa", "inactiva", name="estado_etiqueta"), default="activa")
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
