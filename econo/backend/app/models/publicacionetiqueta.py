from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from backend.app.db.session import Base
import enum

class PublicacionEtiqueta(Base):
    __tablename__ = "publicacion_etiqueta"

    id_publicacion = Column(Integer, ForeignKey("publicacion.id_publicacion"), primary_key=True)
    id_etiqueta = Column(Integer, ForeignKey("etiqueta.id_etiqueta"), primary_key=True)
