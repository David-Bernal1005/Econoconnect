from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class Reaccion(Base):
    __tablename__ = "reacciones"

    id_reaccion = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    Id_Noticia = Column(Integer, ForeignKey("noticias.Id_Noticia"), nullable=False)
    tipo_reaccion = Column(String(20), default="like")
    fecha_reaccion = Column(TIMESTAMP, server_default=func.now())
