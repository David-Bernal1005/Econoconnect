from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from backend.app.db.session import Base

class Noticia(Base):
    __tablename__ = "noticias"

    Id_Noticia = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200))
    resumen = Column(Text)
    enlace = Column(String(500))
    fecha_publicacion = Column(TIMESTAMP, server_default=func.now())
    Id_Categoria = Column(Integer, ForeignKey("categorias.Id_Categoria"))
    Id_Fuente = Column(Integer, ForeignKey("fuentes.Id_Fuente"))
    cantidad_comentarios = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
