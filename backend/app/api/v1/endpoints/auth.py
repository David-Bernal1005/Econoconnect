from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import RegisterRequest, LoginRequest, UserResponse
from app.models.user import RoleEnum, User
from app.services.user_service import get_user_by_username, create_user
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="El username ya existe")

    user = create_user(
        db,
        name=payload.name,
        lastname=payload.lastname,
        cellphone=payload.cellphone,
        direction=payload.direction,
        username=payload.username,
        password=payload.password,
        rol=payload.rol,
        email=payload.email,
    )
    return user

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user: User | None = get_user_by_username(db, payload.username)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_access_token({"sub": user.username, "rol": user.rol.value})
    return {"access_token": token, "token_type": "bearer"}
