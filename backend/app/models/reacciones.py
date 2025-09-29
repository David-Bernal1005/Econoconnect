from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from . import Base

class Reaccion(Base):
    __tablename__ = "reacciones"

    id_reaccion = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    Id_Noticia = Column(Integer, ForeignKey("noticias.Id_Noticia"), nullable=False)
    tipo_reaccion = Column(String(20), default="like")
    fecha_reaccion = Column(TIMESTAMP, server_default=func.now())
