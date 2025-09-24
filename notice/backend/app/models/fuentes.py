from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Fuente(Base):
    __tablename__ = "fuentes"

    Id_Fuente = Column(Integer, primary_key=True, autoincrement=True)
    Nombre_Fuente = Column(String(100))
    Url_Fuente = Column(String(500))
    Tipo_Fuente = Column(String(50))
