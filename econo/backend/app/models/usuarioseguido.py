from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from backend.app.db.session import Base

class UsuarioSeguido(Base):
    __tablename__ = "usuario_seguido"

    id_user = Column(Integer, ForeignKey("users.id_user"), primary_key=True)
    id_user_seguido = Column(Integer, ForeignKey("users.id_user"), primary_key=True)
    fecha_seguimiento = Column(TIMESTAMP, server_default=func.now())
