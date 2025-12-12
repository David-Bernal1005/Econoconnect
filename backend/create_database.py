"""Script para crear la base de datos econoconnect si no existe.

Usa la misma cadena de conexión que el backend (settings.DATABASE_URL),
pero se conecta al servidor sin especificar la BD para poder hacer
"CREATE DATABASE IF NOT EXISTS".
"""

from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
from app.core.config import settings


def create_database_from_scratch() -> None:
	"""Elimina la base de datos destino y la crea de nuevo desde cero."""
	if not settings.DATABASE_URL:
		raise RuntimeError("DATABASE_URL no está configurado en el entorno")

	url = make_url(settings.DATABASE_URL)
	# Nombre de la BD (por ejemplo 'econoconnect')
	db_name = url.database
	# URL al servidor sin BD, para poder ejecutar DROP/CREATE DATABASE
	server_url = url.set(database=None)

	engine = create_engine(server_url)
	with engine.connect() as conn:
		conn.execute(text(f"DROP DATABASE IF EXISTS `{db_name}`"))
		conn.execute(
			text(
				f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
			)
		)
		print(f"✅ Base de datos '{db_name}' recreada desde cero correctamente")


if __name__ == "__main__":
	create_database_from_scratch()
