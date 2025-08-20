from pymongo import MongoClient
from app.core.config import settings

# Crear cliente Mongo
client = MongoClient(settings.MONGO_URL)

# Base de datos
db = client[settings.MONGO_DB_NAME]
