from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.schemas.user import RegisterRequest, LoginRequest, UserResponse
from backend.app.models.user import RoleEnum, User
from backend.app.services.user_service import get_user_by_username, create_user
from backend.app.core.security import verify_password, create_access_token
from backend.app.models.user import StateUser

router = APIRouter()
# Rutas de autenticación

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
    return {"access_token": token, "token_type": "bearer"}
