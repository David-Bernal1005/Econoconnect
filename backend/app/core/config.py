import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Econoconnect"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "clave_super_secreta")  # Cambiar en producción

settings = Settings()