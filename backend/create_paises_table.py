# """
# Script para crear la tabla de países y poblacionarla con datos
# """
# from sqlalchemy import create_engine, text
# from app.core.config import settings

# # Crear la conexión a la base de datos
# engine = create_engine(settings.DATABASE_URL)

# def create_paises_table():
#     with engine.connect() as connection:
#         # Crear tabla paises
#         connection.execute(text("""
#             CREATE TABLE IF NOT EXISTS paises (
#                 id_pais INT AUTO_INCREMENT PRIMARY KEY,
#                 nombre VARCHAR(100) NOT NULL UNIQUE,
#                 codigo_iso VARCHAR(3) UNIQUE,
#                 codigo_telefono VARCHAR(10),
#                 INDEX idx_paises_id_pais (id_pais)
#             )
#         """))
        
#         # Agregar columna id_pais a la tabla users si no existe
#         try:
#             connection.execute(text("""
#                 ALTER TABLE users 
#                 ADD COLUMN id_pais INT,
#                 ADD FOREIGN KEY (id_pais) REFERENCES paises(id_pais)
#             """))
#         except Exception as e:
#             print(f"Columna id_pais ya existe o error: {e}")
        
#         # Insertar países
#         connection.execute(text("""
#             INSERT IGNORE INTO paises (nombre, codigo_iso, codigo_telefono) VALUES
#             ('Colombia', 'COL', '+57'),
#             ('Estados Unidos', 'USA', '+1'),
#             ('México', 'MEX', '+52'),
#             ('Argentina', 'ARG', '+54'),
#             ('Brasil', 'BRA', '+55'),
#             ('Chile', 'CHL', '+56'),
#             ('Perú', 'PER', '+51'),
#             ('Ecuador', 'ECU', '+593'),
#             ('Venezuela', 'VEN', '+58'),
#             ('España', 'ESP', '+34'),
#             ('Francia', 'FRA', '+33'),
#             ('Reino Unido', 'GBR', '+44'),
#             ('Alemania', 'DEU', '+49'),
#             ('Italia', 'ITA', '+39'),
#             ('Canadá', 'CAN', '+1'),
#             ('Australia', 'AUS', '+61'),
#             ('Japón', 'JPN', '+81'),
#             ('China', 'CHN', '+86'),
#             ('India', 'IND', '+91'),
#             ('Rusia', 'RUS', '+7')
#         """))
        
#         connection.commit()
#         print("✅ Tabla de países creada e inicializada correctamente")

# if __name__ == "__main__":
#     create_paises_table()