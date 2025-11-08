
from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

# Endpoint para obtener el rol del usuario autenticado
@router.get("/user/roles")
async def get_user_roles(current_user: User = Depends(get_current_user)):
    return {"rol": str(current_user.rol)}
