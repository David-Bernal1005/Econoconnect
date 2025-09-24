import sys
import os
from logging.config import fileConfig

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from alembic import context
from sqlalchemy import engine_from_config, pool

# Importar engine, MARIADB_URL y Base
from app.db.session import engine, MARIADB_URL, Base

# Importar el modelo User
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
#from app.models.notificaciones import Notificacion
from app.models.publicacion import Publicacion
from app.models.publicacionadjunto import PublicacionAdjunto
from app.models.publicacionetiqueta import PublicacionEtiqueta
from app.models.reacciones import Reaccion
from app.models.rol import Rol
from app.models.tiposcontenido import TipoContenido
from app.models.usuariorol import UsuarioRol
from app.models.usuarioseguidor import UsuarioSeguidor
from app.models.usuarioseguido import UsuarioSeguido

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