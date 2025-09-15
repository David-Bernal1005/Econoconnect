from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from backend.app.db.session import Base
import enum

class ComentarioNoticia(Base):
    __tablename__ = "comentarios_noticias"

    id_comentario = Column(Integer, primary_key=True, autoincrement=True)
    Id_Noticia = Column(Integer, ForeignKey("noticias.Id_Noticia"))
    texto = Column(Text)
    fecha_comentario = Column(TIMESTAMP, server_default=func.now())
