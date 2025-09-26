from sqlalchemy import Column, Integer, String, Text
from . import Base

class TipoContenido(Base):
    __tablename__ = "tipos_contenido"

    Id_Tipo = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_Tipo = Column(String(50))
    Descripcion = Column(Text)
