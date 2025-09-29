from sqlalchemy import Column, Integer, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class Comentario(Base):
    __tablename__ = "comentario"

    id_comentario = Column(Integer, primary_key=True, autoincrement=True)
    publicacion_id = Column(Integer, ForeignKey("publicacion.id_publicacion"))
    id_user = Column(Integer, ForeignKey("users.id_user"))
    contenido = Column(Text)
    estado = Column(Enum("activo", "eliminado", name="estado_comentario"), default="activo")
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    foro = relationship("Foro", back_populates="comentarios")
    autor = relationship("User", back_populates="comentarios")