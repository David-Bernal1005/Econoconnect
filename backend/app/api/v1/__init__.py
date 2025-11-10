from fastapi import APIRouter
from .endpoints import (
    foro,
    foro_ws,
    # otros endpoints aquí...
)

api_router = APIRouter()
api_router.include_router(foro.router)
api_router.include_router(foro_ws.router)