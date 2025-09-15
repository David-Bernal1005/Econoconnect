from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from backend.app.db.session import Base
import enum

class ChatMensajeAdjunto(Base):
    __tablename__ = "chat_mensaje_adjunto"

    id_mensaje = Column(Integer, ForeignKey("chat_mensaje.id_mensaje"), primary_key=True)
    id_adjunto = Column(Integer, ForeignKey("adjunto.id_adjunto"), primary_key=True)
