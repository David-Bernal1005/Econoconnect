from sqlalchemy import text
from app.db.session import engine

with engine.connect() as conn:
    result = conn.execute(text("SHOW TABLES")).fetchall()
    print("Tablas en la base de datos:")
    for row in result:
        print(row[0])
