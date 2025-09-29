from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base
import enum

class EstadoForo(enum.Enum):
    activo = "activo"
    inactivo = "inactivo"

class Foro(Base):
    __tablename__ = "foro"
    id_foro = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(450))
    autor_id = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    estado = Column(Enum(EstadoForo), default=EstadoForo.activo, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    grafica_id = Column(Integer, ForeignKey("grafica.id_grafica"), unique=True, nullable=False)
    autor = relationship("User", back_populates="foros")
    grafica = relationship("Grafica", back_populates="foro")
    comentarios = relationship("Comentario", back_populates="foro", cascade="all, delete-orphan")
