from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.models import Comentario, user as user_model
from app.db.session import get_db
from datetime import datetime
import json
from jose import JWTError, jwt
from app.core.config import settings

router = APIRouter(prefix="/ws/foro", tags=["Foro WS"])

active_connections: dict[int, list[WebSocket]] = {}


async def _accept_and_register(websocket: WebSocket, foro_id: int):
    await websocket.accept()
    if foro_id not in active_connections:
        active_connections[foro_id] = []
    active_connections[foro_id].append(websocket)


async def _unregister(websocket: WebSocket, foro_id: int):
    if foro_id in active_connections and websocket in active_connections[foro_id]:
        active_connections[foro_id].remove(websocket)
        if not active_connections[foro_id]:
            del active_connections[foro_id]


async def broadcast_message(foro_id: int, message: dict):
    if foro_id in active_connections:
        for connection in list(active_connections[foro_id]):
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                # ignore send errors for now
                pass


def _get_user_from_token(token: str, db: Session):
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if not username:
            return None
    except JWTError:
        return None
    # fetch user
    user = db.query(user_model.User).filter(user_model.User.username == username).first()
    return user


@router.websocket("/{foro_id}")
async def foro_websocket(websocket: WebSocket, foro_id: int, db: Session = Depends(get_db)):
    # Esperar token en query params: ws://.../ws/foro/{id}?token=...
    token = websocket.query_params.get("token")
    user = _get_user_from_token(token, db)
    if not user:
        # cerrar con código 1008 (policy violation)
        await websocket.close(code=1008)
        return

    # Registrar conexión autenticada
    await _accept_and_register(websocket, foro_id)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            contenido = payload.get("contenido")
            if not contenido or not contenido.strip():
                # ignorar mensajes vacíos
                continue

            # Crear el nuevo comentario usando el usuario autenticado
            try:
                # Verificar si el foro existe
                from app.models.foro import Foro
                foro = db.query(Foro).filter(Foro.id_foro == foro_id).first()
                if not foro:
                    await websocket.send_text(json.dumps({"error": "El foro no existe"}))
                    continue

                nuevo_comentario = Comentario(
                    foro_id=foro_id,
                    id_user=user.id_user,
                    contenido=contenido.strip(),
                    estado="activo",
                    fecha_creacion=datetime.now()
                )
                db.add(nuevo_comentario)
                db.commit()
                db.refresh(nuevo_comentario)

                message = {
                    "id_comentario": getattr(nuevo_comentario, 'id_comentario', None),
                    "id_user": getattr(nuevo_comentario, 'id_user', None),
                    "username": getattr(user, 'username', None),
                    "contenido": nuevo_comentario.contenido,
                    "fecha_creacion": str(nuevo_comentario.fecha_creacion)
                }

                await broadcast_message(foro_id, message)
            except Exception as e:
                # Log and send an error back to the sender connection
                error_message = str(e)
                try:
                    error_details = "No se pudo guardar el comentario"
                    if "foreign key constraint" in error_message.lower():
                        error_details = "Error de referencia: verifica que el foro existe"
                    elif "null value in column" in error_message.lower():
                        error_details = "Faltan datos requeridos para crear el comentario"
                    
                    await websocket.send_text(json.dumps({
                        "error": error_details,
                        "details": str(e)
                    }))
                except Exception:
                    pass
                # rollback and log
                try:
                    db.rollback()
                except Exception:
                    pass
                logger = __import__('logging').getLogger(__name__)
                logger.error(f"Error guardando comentario: {e}")

    except WebSocketDisconnect:
        await _unregister(websocket, foro_id)



