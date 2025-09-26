from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth, noticias, publicaciones, graficas

app = FastAPI(title="Econoconnect")

# Endpoint para listar todos los endpoints registrados
@app.get("/endpoints")
def list_endpoints():
    return [
        {"path": route.path, "methods": list(route.methods)}
        for route in app.router.routes
    ]

# Middleware CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(noticias.router, prefix="/api/v1")
app.include_router(publicaciones.router, prefix="/api/v1")
app.include_router(graficas.router, prefix="/api/v1", tags=["graficas"])