from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from backend.app.db.session import Base
import enum

class ComentarioAdjunto(Base):
    __tablename__ = "comentario_adjunto"

    id_comentario = Column(Integer, ForeignKey("comentario.id_comentario"), primary_key=True)
    id_adjunto = Column(Integer, ForeignKey("adjunto.id_adjunto"), primary_key=True)
