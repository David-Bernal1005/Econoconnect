from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User
from app.models.adjunto import Adjunto
from app.models.auditoriausuarioestado import AuditoriaUsuarioEstado
from app.models.categorias import Categoria
from app.models.chat import Chat
from app.models.chatmensaje import ChatMensaje
from app.models.chatmensajeadjunto import ChatMensajeAdjunto
from app.models.chatmiembro import ChatMiembro
from app.models.comentario import Comentario
from app.models.comentarionoticias import ComentarioNoticia
from app.models.comentariopublicaciones import ComentarioPublicacion
from app.models.cometarioadjunto import ComentarioAdjunto
from app.models.datografica import DatoGrafica
from app.models.etiqueta import Etiqueta
from app.models.foro import Foro
from app.models.fuentes import Fuente
from app.models.grafica import Grafica
from app.models.noticias import Noticia
from app.models.publicacion import Publicacion
from app.models.publicacionadjunto import PublicacionAdjunto
from app.models.publicacionetiqueta import PublicacionEtiqueta
from app.models.reacciones import Reaccion
from app.models.rol import Rol
from app.models.tiposcontenido import TipoContenido
from app.models.usuariorol import UsuarioRol
from app.models.usuarioseguidor import UsuarioSeguidor
from app.models.usuarioseguido import UsuarioSeguido

