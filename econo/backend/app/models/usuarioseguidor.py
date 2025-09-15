from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from backend.app.db.session import Base

class UsuarioSeguidor(Base):
    __tablename__ = "usuario_seguidor"

    id_user = Column(Integer, ForeignKey("users.id_user"), primary_key=True)
    id_user_seguidor = Column(Integer, ForeignKey("users.id_user"), primary_key=True)
    fecha_seguimiento = Column(TIMESTAMP, server_default=func.now())
