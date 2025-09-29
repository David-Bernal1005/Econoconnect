from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import RegisterRequest, LoginRequest, UserResponse
from app.models.user import User
from app.services.user_service import get_user_by_username, create_user
from app.core.security import verify_password, create_access_token
from app.models.user import StateUser

router = APIRouter()

# --- Password reset code storage (demo: in-memory, use DB/cache in prod) ---

import random, string, time
from fastapi import BackgroundTasks
from app.core.security import get_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# reset_codes = {email: (code, timestamp)}
reset_codes = {}  # {email: (code, timestamp)}

# --- Configuración SMTP (Gmail) ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Puerto para Gmail con STARTTLS
SMTP_USER = "brandonquintero028@gmail.com"  # Cambia por el correo que enviará los mensajes
SMTP_PASS = "cnsc hkwo sofj qked"  # Cambia por la contraseña de aplicación de Gmail

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        print(f"Correo enviado a {to_email}")
    except Exception as e:
        print(f"Error enviando correo: {e}")

# --- Endpoint: request password reset ---
from pydantic import EmailStr
class PasswordResetRequest(BaseModel):
    email: EmailStr

@router.post("/forgot-password")
def forgot_password(payload: PasswordResetRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="¡Ups! No encontramos tu usuario en Econoconnect. ¿El correo está bien?")
    code = ''.join(random.choices(string.digits, k=6))
    timestamp = time.time()
    reset_codes[payload.email] = (code, timestamp)
    background_tasks.add_task(send_email, payload.email, "Recupera tu acceso a Econoconnect", f"¡Hola! Tu código de recuperación es: {code}. Ingresa este código en la app para cambiar tu contraseña. El código expira en 3 minutos.")
    return {"msg": "¡Listo! Te enviamos el código a tu correo. Revisa tu bandeja y sigue las instrucciones para recuperar tu acceso a Econoconnect."}

# --- Endpoint: validate code and change password ---
class PasswordChangeRequest(BaseModel):
    email: EmailStr
    code: str
    new_password: str

@router.post("/reset-password")
def reset_password(payload: PasswordChangeRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="¡Ups! No encontramos tu usuario en Econoconnect.")
    code_data = reset_codes.get(payload.email)
    if not code_data:
        raise HTTPException(status_code=400, detail="No se ha solicitado código de recuperación o ya expiró.")
    code, timestamp = code_data
    # Expiración de 3 minutos
    if time.time() - timestamp > 180:
        reset_codes.pop(payload.email, None)
        raise HTTPException(status_code=400, detail="El código ha expirado. Solicita uno nuevo.")
    if code != payload.code:
        raise HTTPException(status_code=400, detail="Código inválido. Verifica el código enviado a tu correo.")
    # No permitir la misma contraseña
    if user.hashed_password == get_password_hash(payload.new_password):
        raise HTTPException(status_code=400, detail="Por seguridad, tu nueva contraseña debe ser diferente a la anterior.")
    user.hashed_password = get_password_hash(payload.new_password)
    db.commit()
    reset_codes.pop(payload.email, None)
    return {"msg": "¡Contraseña actualizada! Ahora puedes iniciar sesión en Econoconnect con tu nueva clave."}

@router.post("/register", response_model=UserResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    print(f"Datos recibidos en registro: {payload}")

    if get_user_by_username(db, payload.username):
        print("El username ya existe")
        raise HTTPException(status_code=400, detail="El username ya existe")

    # Verificar email duplicado
    if payload.email:
        existing_email = db.query(User).filter(User.email == payload.email).first()
        if existing_email:
            print("El email ya existe")
            raise HTTPException(status_code=400, detail="El email ya existe")

    user = create_user(
        db,
        name=payload.name,
        lastname=payload.lastname,
        cellphone=payload.cellphone,
        direction=payload.direction,
        username=payload.username,
        password=payload.password,
        rol=payload.rol,
        country=payload.country,
        email=payload.email,
    state=StateUser.activo,
        creation_date=func.now(),
        last_activity_date=None,
        number_followers=0
    )
    print(f"Usuario creado: {user}")
    return user

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user: User | None = get_user_by_username(db, payload.username)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = create_access_token({"sub": user.username, "rol": user.rol.value})
    return {
        "access_token": token,
        "token_type": "bearer",
        "name": user.name,
        "id_user": user.id_user
    }
