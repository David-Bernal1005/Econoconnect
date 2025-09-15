from sqlalchemy import Column, Integer, String, Enum, UniqueConstraint
from sqlalchemy.sql import func
from backend.app.db.session import Base
from enum import Enum as PyEnum
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import relationship

class StateUser(PyEnum):
    Activo = "activo"
    Inactivo = "inactivo"
class RoleEnum(str, PyEnum):
    administrador = "administrador"
    usuario = "usuario"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("email", name="uq_users_email"),
    )

    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    cellphone = Column(String(20), nullable=False)
    direction = Column(String(120), nullable=False)
    username = Column(String(50), nullable=False, index=True)
    email = Column(String(120), nullable=True)  # opcional si no lo usas
    hashed_password = Column(String(255), nullable=False)
    country = Column(String(50), nullable=False)
    rol = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.usuario)
    state = Column(Enum(StateUser), default=StateUser.Activo, nullable=False)
    creation_date = Column(TIMESTAMP, default=func.now(), nullable=False)
    last_activity_date = Column(TIMESTAMP, default=func.now(), nullable=False)
    number_followers = Column(Integer, default=0)

    foros = relationship("Foro", back_populates="autor")
