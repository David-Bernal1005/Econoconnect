from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import get_user_by_username
from jose import JWTError, jwt
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


from app.schemas.user import UserUpdateRequest

@router.put("/me", response_model=UserResponse)
async def update_user_me(
    payload: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.name = payload.name
    current_user.lastname = payload.lastname
    current_user.email = payload.email
    current_user.cellphone = payload.cellphone
    current_user.direction = payload.direction
    current_user.country = payload.country
    if payload.profile_image is not None:
        current_user.profile_image = payload.profile_image
    db.commit()
    db.refresh(current_user)
    return current_user
