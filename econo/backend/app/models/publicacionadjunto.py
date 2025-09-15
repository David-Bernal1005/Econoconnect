from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from backend.app.db.session import Base
import enum

class PublicacionAdjunto(Base):
    __tablename__ = "publicacion_adjunto"

    id_publicacion = Column(Integer, ForeignKey("publicacion.id_publicacion"), primary_key=True)
    id_adjunto = Column(Integer, ForeignKey("adjunto.id_adjunto"), primary_key=True)
