from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from backend.app.db.session import Base
import enum

class ComentarioPublicacion(Base):
    __tablename__ = "comentarios_publicaciones"

    id_comentario = Column(Integer, primary_key=True, autoincrement=True)
    Id_Publicacion = Column(Integer, ForeignKey("publicacion.id_publicacion"))
    texto = Column(Text)
    fecha_comentario = Column(TIMESTAMP, server_default=func.now())
