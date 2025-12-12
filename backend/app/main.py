from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import (
    auth, noticias, publicaciones, graficas, user, user_update,
    chat, chat_ws, etiquetas, paises, foro, foro_ws, chatmiembros, seguidores
)



app = FastAPI(title="Econoconnect")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Endpoint para listar todos los endpoints registrados
@app.get("/endpoints")
def list_endpoints():
    return [
        {"path": route.path, "methods": list(route.methods)}
        for route in app.router.routes
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(chatmiembros.router, prefix="/api/v1")
app.include_router(chat_ws.router)
app.include_router(foro_ws.router)  # El router de foro_ws incluye su propio prefijo
app.include_router(foro.router, prefix="/api/v1")
app.include_router(noticias.router, prefix="/api/v1")
app.include_router(publicaciones.router, prefix="/api/v1")
app.include_router(graficas.router, prefix="/api/v1", tags=["graficas"])
app.include_router(user.router, prefix="/api/v1")
app.include_router(user_update.router, prefix="/api/v1/users", tags=["users"])
app.include_router(etiquetas.router, prefix="/api/v1")
app.include_router(paises.router, prefix="/api/v1", tags=["paises"])
app.include_router(seguidores.router, prefix="/api/v1")  # Agrega el router de seguidores