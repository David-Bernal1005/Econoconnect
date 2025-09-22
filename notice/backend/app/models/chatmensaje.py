from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from backend.app.db.session import Base
import enum

class ChatMensaje(Base):
    __tablename__ = "chat_mensaje"

    id_mensaje = Column(Integer, primary_key=True, autoincrement=True)
    id_chat = Column(Integer, ForeignKey("chat.id_chat"))
    id_user = Column(Integer, ForeignKey("users.id_user"))
    contenido = Column(Text)
    fecha_envio = Column(DATETIME, server_default=func.now())
    estado = Column(Enum("enviado", "leido", "eliminado", name="estado_mensaje"), default="enviado")
