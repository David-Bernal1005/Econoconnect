from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from backend.app.db.session import Base, engine
from backend.app.api.v1.endpoints import auth

app = FastAPI(title="Econoconnect")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajusta en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth")