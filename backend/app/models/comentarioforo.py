from sqlalchemy import Column, Integer, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class Comentario(Base):
    __tablename__ = "comentario"

    id_comentario = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id_user"))
    id_foro = Column(Integer, ForeignKey("foro.id_foro"))
    contenido = Column(Text)
    estado = Column(Enum("activo", "eliminado", name="estado_comentario"), default="activo")
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    foro = relationship("Foro", back_populates="comentarios")
    autor = relationship("User", foreign_keys=[id_user], back_populates="comentarios")