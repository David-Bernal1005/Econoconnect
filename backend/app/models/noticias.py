from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from . import Base

class Noticia(Base):
    __tablename__ = "noticias"

    Id_Noticia = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200))
    resumen = Column(Text)
    enlace = Column(String(500))
    fecha_publicacion = Column(TIMESTAMP, server_default=func.now())
    Id_Categoria = Column(Integer, ForeignKey("categorias.Id_Categoria"))
    Id_Fuente = Column(Integer, ForeignKey("fuentes.Id_Fuente"))
    usuario = Column(String(100))
    activa = Column(Integer, default=1)  # 1=activa, 0=inactiva
    profile_image = Column(String(length=1000000), nullable=True)  # base64
