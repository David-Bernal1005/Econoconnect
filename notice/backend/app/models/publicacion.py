from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.session import Base

class Publicacion(Base):
    __tablename__ = "publicacion"

    id_publicacion = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id_user"))
    foro_id = Column(Integer, ForeignKey("foro.id_foro"))
    titulo = Column(String(200))
    contenido = Column(Text)
    estado = Column(Enum("publicada", "eliminada", "archivada", name="estado_publicacion"), default="publicada")
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    cantidad_comentarios = Column(Integer, default=0)
    slug = Column(String(255))
    fecha_ultima_actividad = Column(TIMESTAMP)
