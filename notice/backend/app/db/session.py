
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Usar la cadena de conexión de .env
MARIADB_URL = settings.DATABASE_URL or "mysql+pymysql://root:@localhost:3306/econoconnect"

engine = create_engine(MARIADB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
