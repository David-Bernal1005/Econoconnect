from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class EstadoForo(enum.Enum):
    activo = "activo"
    inactivo = "inactivo"

class Foro(Base):
    __tablename__ = "foro"
    __table_args__ = {'extend_existing': True}

    id_foro = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(450))
    autor_id = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    estado = Column(Enum(EstadoForo), default=EstadoForo.activo)
    fecha_creacion = Column(TIMESTAMP)

    autor = relationship("User", back_populates="foros")
