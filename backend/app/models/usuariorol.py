from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class UsuarioRol(Base):
    __tablename__ = "usuario_rol"

    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    id_rol = Column(Integer, ForeignKey("rol.id_rol"), primary_key=True)
