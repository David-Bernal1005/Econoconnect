from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from . import Base

class DatoGrafica(Base):
    __tablename__ = "dato_grafica"

    id_dato = Column(Integer, primary_key=True, autoincrement=True)
    id_grafica = Column(Integer, ForeignKey("grafica.id_grafica"))
    anio = Column(Integer)
    cop_usd = Column(DECIMAL(15, 2))
    cop_eur = Column(DECIMAL(15, 2))
    fecha_actualizacion = Column(Date)
    etiqueta = Column(String(100))
    fecha = Column(Date)
    valor = Column(DECIMAL(15, 2))
    
#INSERT INTO dato_grafica (id_grafica, etiqueta, fecha, valor, anio, cop_usd, cop_eur, fecha_actualizacion)
#VALUES
#-- 2018
#(1, 'COP/USD', '2018-01-01', 2976.50, 2018, 2976.50, 3675.59, '2018-12-31'),
#(1, 'COP/EUR', '2018-01-01', 3675.59, 2018, 2976.50, 3675.59, '2018-12-31'),
#
#-- 2019
#(1, 'COP/USD', '2019-01-01', 3357.60, 2019, 3357.60, 3788.65, '2019-12-31'),
#(1, 'COP/EUR', '2019-01-01', 3788.65, 2019, 3357.60, 3788.65, '2019-12-31'),
#
#-- 2020
#(1, 'COP/USD', '2020-01-01', 3688.67, 2020, 3688.67, 4183.67, '2020-12-31'),
#(1, 'COP/EUR', '2020-01-01', 4183.67, 2020, 3688.67, 4183.67, '2020-12-31'),
#
#-- 2021
#(1, 'COP/USD', '2021-01-01', 3830.49, 2021, 3830.49, 4392.50, '2021-12-31'),
#(1, 'COP/EUR', '2021-01-01', 4392.50, 2021, 3830.49, 4392.50, '2021-12-31'),
#
#-- 2022
#(1, 'COP/USD', '2022-01-01', 4392.50, 2022, 4392.50, 4392.50, '2022-12-31'),
#(1, 'COP/EUR', '2022-01-01', 4392.50, 2022, 4392.50, 4392.50, '2022-12-31'),
#
#-- 2023
#(1, 'COP/USD', '2023-01-01', 3977.57, 2023, 3977.57, 4275.26, '2023-12-31'),
#(1, 'COP/EUR', '2023-01-01', 4275.26, 2023, 3977.57, 4275.26, '2023-12-31'),
#
#-- 2024
#(1, 'COP/USD', '2024-01-01', 4081.12, 2024, 4081.12, 4409.81, '2024-12-31'),
#(1, 'COP/EUR', '2024-01-01', 4409.81, 2024, 4081.12, 4409.81, '2024-12-31'),
#
#-- 2025 (proyección actual)
#(1, 'COP/USD', '2025-01-01', 3874.63, 2025, 3874.63, 4426.37, '2025-11-09'),
#(1, 'COP/EUR', '2025-01-01', 4426.37, 2025, 3874.63, 4426.37, '2025-11-09');
