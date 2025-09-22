from sqlalchemy import Column, Integer, ForeignKey
from backend.app.db.session import Base

class ComentarioAdjunto(Base):
    __tablename__ = "comentario_adjunto"

    id_comentario = Column(Integer, ForeignKey("comentario.id_comentario"), primary_key=True)
    id_adjunto = Column(Integer, ForeignKey("adjunto.id_adjunto"), primary_key=True)
