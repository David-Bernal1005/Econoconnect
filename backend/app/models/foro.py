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
    id_grafica = Column(Integer, ForeignKey("grafica.id_grafica"), nullable=True)
    autor = relationship("User", back_populates="foros")
    grafica = relationship("Grafica", back_populates="foros")
    comentarios = relationship("Comentario", back_populates="foro", cascade="all, delete-orphan")

#INSERT INTO foro (nombre, descripcion, autor_id, estado, fecha_creacion, id_grafica)
#VALUES (
#    'Evolución del Dólar y Euro frente al Peso Colombiano (2018–2025)',
#    'Análisis comparativo de las tasas de cambio COP/USD y COP/EUR entre 2018 y 2025, mostrando cómo las variaciones del mercado internacional han afectado el valor del peso colombiano.',
#    1,
#    'activo',
#    NOW(),
#    1
#);