"""Script para asegurarse de que la tabla de países existe
y está poblada con datos base.

Se apoya en la configuración de SQLAlchemy de la app
para reutilizar la misma cadena de conexión.
"""

from sqlalchemy import create_engine, text
from app.core.config import settings


engine = create_engine(settings.DATABASE_URL)


def create_paises_table() -> None:

	with engine.begin() as connection:
		# Crear tabla paises (por seguridad, aunque Alembic ya la crea)
		connection.execute(
			text(
				"""
				CREATE TABLE IF NOT EXISTS paises (
					id_pais INT AUTO_INCREMENT PRIMARY KEY,
					nombre VARCHAR(100) NOT NULL UNIQUE,
					codigo_iso VARCHAR(3) UNIQUE,
					codigo_telefono VARCHAR(10),
					INDEX idx_paises_id_pais (id_pais)
				)
				"""
			)
		)

		# Insertar países base (IGNORE evita duplicados si ya existían)
		connection.execute(
			text(
				"""
				INSERT IGNORE INTO paises (nombre, codigo_iso, codigo_telefono) VALUES
				('Colombia', 'COL', '+57'),
				('Estados Unidos', 'USA', '+1'),
				('México', 'MEX', '+52'),
				('Argentina', 'ARG', '+54'),
				('Brasil', 'BRA', '+55'),
				('Chile', 'CHL', '+56'),
				('Perú', 'PER', '+51'),
				('Ecuador', 'ECU', '+593'),
				('Venezuela', 'VEN', '+58'),
				('España', 'ESP', '+34'),
				('Francia', 'FRA', '+33'),
				('Reino Unido', 'GBR', '+44'),
				('Alemania', 'DEU', '+49'),
				('Italia', 'ITA', '+39'),
				('Canadá', 'CAN', '+1'),
				('Australia', 'AUS', '+61'),
				('Japón', 'JPN', '+81'),
				('China', 'CHN', '+86'),
				('India', 'IND', '+91'),
				('Rusia', 'RUS', '+7')
				"""
			)
		)

	print("✅ Tabla de países creada e inicializada correctamente")


if __name__ == "__main__":
	create_paises_table()