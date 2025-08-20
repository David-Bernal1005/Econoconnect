from werkzeug.security import generate_password_hash
from app.api.v1.endpoints.auth import RoleEnum
from app.db.session import users_collection

def create_user(name: str, lastname: str, cellphone: str, direction: str, username: str, password: str, rol: RoleEnum):
    # Hashear la contraseña
    hashed_password = generate_password_hash(password)
    
    # Documento a insertar en Mongo
    new_user = {
        "name": name,
        "lastname": lastname,
        "cellphone": cellphone,
        "direction": direction,
        "username": username,
        "password": hashed_password,
        "rol": rol.value  # Guardamos el valor del Enum ("administrador" o "usuario")
    }

    # Insertar en la colección
    result = users_collection.insert_one(new_user)
    # Devolver el documento con su _id en formato string
    new_user["_id"] = str(result.inserted_id)
    return new_user

def get_user_by_username(username: str):
    user = users_collection.find_one({"username": username})
    if user:
        user["_id"] = str(user["_id"])
    return user