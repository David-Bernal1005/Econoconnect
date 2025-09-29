from sqlalchemy import Column, Integer, ForeignKey
from . import Base

class UsuarioRol(Base):
    __tablename__ = "usuario_rol"

    id_user = Column(Integer, ForeignKey("users.id_user"), primary_key=True)
    id_rol = Column(Integer, ForeignKey("rol.id_rol"), primary_key=True)
