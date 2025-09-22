from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from backend.app.db.session import Base
import enum

class Chat(Base):
    __tablename__ = "chat"

    id_chat = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    tipo = Column(Enum("privado", "grupo", name="tipo_chat"), default="privado")
    descripcion = Column(Text)
    creador_id = Column(Integer, ForeignKey("users.id_user"))
    estado = Column(Enum("activo", "inactivo", name="estado_chat"), default="activo")
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
