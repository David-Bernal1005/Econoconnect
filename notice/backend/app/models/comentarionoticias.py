from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from backend.app.db.session import Base

class ComentarioNoticia(Base):
    __tablename__ = "comentarios_noticias"

    id_comentario = Column(Integer, primary_key=True, autoincrement=True)
    Id_Noticia = Column(Integer, ForeignKey("noticias.Id_Noticia"))
    texto = Column(Text)
    fecha_comentario = Column(TIMESTAMP, server_default=func.now())
