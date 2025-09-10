from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base

class UsuarioSeguido(Base):
    __tablename__ = "usuario_seguido"

    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    id_usuario_seguido = Column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    fecha_seguimiento = Column(TIMESTAMP, server_default=func.now())
