from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from . import Base

class ComentarioPublicacion(Base):
    __tablename__ = "comentarios_publicaciones"

    id_comentario = Column(Integer, primary_key=True, autoincrement=True)
    Id_Publicacion = Column(Integer, ForeignKey("publicacion.id_publicacion"))
    texto = Column(Text)
    fecha_comentario = Column(TIMESTAMP, server_default=func.now())
