from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base

class Grafica(Base):
    __tablename__ = "grafica"

    id_grafica = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200))
    descripcion = Column(Text)
    tipo_grafica = Column(String(50))
    autor_id = Column(Integer, ForeignKey("users.id_user"))
    estado = Column(Enum("activa", "inactiva", name="estado_grafica"), default="activa")
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    foro = relationship("Foro", back_populates="grafica", uselist=False)

