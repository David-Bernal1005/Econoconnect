from sqlalchemy import Column, Integer, ForeignKey
from . import Base

class PublicacionAdjunto(Base):
    __tablename__ = "publicacion_adjunto"

    id_publicacion = Column(Integer, ForeignKey("publicacion.id_publicacion"), primary_key=True)
    id_adjunto = Column(Integer, ForeignKey("adjunto.id_adjunto"), primary_key=True)
