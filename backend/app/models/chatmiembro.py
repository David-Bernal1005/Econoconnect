from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.sql import func
from . import Base

class ChatMiembro(Base):
    __tablename__ = "chat_miembro"

    id_chat = Column(Integer, ForeignKey("chat.id_chat"), primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user"), primary_key=True)
    fecha_ingreso = Column(TIMESTAMP, server_default=func.now())
    rol_chat = Column(Enum("admin", "miembro", name="rol_chat"), default="miembro")
