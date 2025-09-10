from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class AuditoriaUsuarioEstado(Base):
    __tablename__ = "auditoria_usuario_estado"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    estado_anterior = Column(Enum("activo", "inactivo", name="estado_anterior"))
    estado_nuevo = Column(Enum("activo", "inactivo", name="estado_nuevo"))
    fecha = Column(TIMESTAMP, server_default=func.now())
