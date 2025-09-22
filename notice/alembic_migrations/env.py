import sys
import os
from logging.config import fileConfig

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from alembic import context
from sqlalchemy import engine_from_config, pool

# Importar engine, MARIADB_URL y Base
from backend.app.db.session import engine, MARIADB_URL, Base

# Importar el modelo User
from backend.app.models.user import User
from backend.app.models.adjunto import Adjunto
from backend.app.models.auditoriausuarioestado import AuditoriaUsuarioEstado
from backend.app.models.categorias import Categoria
from backend.app.models.chat import Chat
from backend.app.models.chatmensaje import ChatMensaje
from backend.app.models.chatmensajeadjunto import ChatMensajeAdjunto
from backend.app.models.chatmiembro import ChatMiembro
from backend.app.models.comentario import Comentario
from backend.app.models.comentarionoticias import ComentarioNoticia
from backend.app.models.comentariopublicaciones import ComentarioPublicacion
from backend.app.models.cometarioadjunto import ComentarioAdjunto
from backend.app.models.datografica import DatoGrafica
from backend.app.models.etiqueta import Etiqueta
from backend.app.models.foro import Foro
from backend.app.models.fuentes import Fuente
from backend.app.models.grafica import Grafica
from backend.app.models.noticias import Noticia
#from backend.app.models.notificaciones import Notificacion
from backend.app.models.publicacion import Publicacion
from backend.app.models.publicacionadjunto import PublicacionAdjunto
from backend.app.models.publicacionetiqueta import PublicacionEtiqueta
from backend.app.models.reacciones import Reaccion
from backend.app.models.rol import Rol
from backend.app.models.tiposcontenido import TipoContenido
from backend.app.models.usuariorol import UsuarioRol
from backend.app.models.usuarioseguidor import UsuarioSeguidor
from backend.app.models.usuarioseguido import UsuarioSeguido

config = context.config

if config.config_file_name is not None:
	fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
	url = config.get_main_option("sqlalchemy.url")
	context.configure(
		url=url,
		target_metadata=target_metadata,
		literal_binds=True,
		dialect_opts={"paramstyle": "named"},
	)
	with context.begin_transaction():
		context.run_migrations()

def run_migrations_online():
	config.set_main_option("sqlalchemy.url", MARIADB_URL)
	connectable = engine_from_config(
		config.get_section(config.config_ini_section, {}),
		prefix="sqlalchemy.",
		poolclass=pool.NullPool,
	)
	with connectable.connect() as connection:
		context.configure(
			connection=connection,
			target_metadata=target_metadata,
			compare_type=True,
		)
		with context.begin_transaction():
			context.run_migrations()

if context.is_offline_mode():
	run_migrations_offline()
else:
	run_migrations_online()