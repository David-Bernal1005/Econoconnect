from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, DECIMAL, Date, BigInteger, DATETIME
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class Categoria(Base):
    __tablename__ = "categorias"

    Id_Categoria = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_Categoria = Column(String(100))
    Descripcion = Column(Text)
