from sqlalchemy import Column, Integer, String
from . import Base

class Pais(Base):
    __tablename__ = "paises"

    id_pais = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    codigo_iso = Column(String(3), nullable=True, unique=True)  # Código ISO 3166-1 alpha-3
    codigo_telefono = Column(String(10), nullable=True)  # Código de teléfono del país (+57, +1, etc.)
    
    def __repr__(self):
        return f"<Pais(id={self.id_pais}, nombre='{self.nombre}', codigo_iso='{self.codigo_iso}')>"