from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.sql import func
from backend.app.db.session import Base
import enum

class AuditoriaUsuarioEstado(Base):
    __tablename__ = "auditoria_usuario_estado"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("users.id_user"))
    estado_anterior = Column(Enum("activo", "inactivo", name="estado_anterior"))
    estado_nuevo = Column(Enum("activo", "inactivo", name="estado_nuevo"))
    fecha = Column(TIMESTAMP, server_default=func.now())
