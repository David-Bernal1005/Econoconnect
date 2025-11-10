from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Comentario, user as user_model, Foro
from app.db.session import get_db
from datetime import datetime
from typing import List
import json
from jose import JWTError, jwt
from app.core.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security
from pydantic import BaseModel

security = HTTPBearer()
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


@router.get("/{foro_id}/comentarios")
async def get_comentarios_foro(
    foro_id: int,
    db: Session = Depends(get_db),
):
    """Devuelve los comentarios activos de un foro. Ruta pública para que la UI cargue
    los comentarios históricos sin necesitar autenticación."""
    # Verificar que el foro existe
    foro = db.query(Foro).filter(Foro.id_foro == foro_id).first()
    if not foro:
        raise HTTPException(status_code=404, detail="Foro no encontrado")

    # Obtener todos los comentarios activos del foro
    comentarios = db.query(Comentario).\
        filter(Comentario.id_foro == foro_id, Comentario.estado == "activo").\
        order_by(Comentario.fecha_creacion.desc()).\
        all()

    # Formatear la respuesta
    return [{
        "id_comentario": comentario.id_comentario,
        "id_user": comentario.id_user,
        "username": comentario.autor.username if comentario.autor else None,
        "contenido": comentario.contenido,
        "fecha_creacion": str(comentario.fecha_creacion)
    } for comentario in comentarios]


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
                    id_foro=foro_id,
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


class ComentarioCreate(BaseModel):
    contenido: str


@router.post("/{foro_id}/comentarios", status_code=201)
async def crear_comentario_rest(
    foro_id: int,
    payload: ComentarioCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """Crear un comentario vía REST (requiere token). Guarda en BD y notifica a conexiones WebSocket activas."""
    # Validar usuario
    user = _get_user_from_token(credentials.credentials, db)
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")

    # Verificar foro
    foro = db.query(Foro).filter(Foro.id_foro == foro_id).first()
    if not foro:
        raise HTTPException(status_code=404, detail="Foro no encontrado")

    contenido = (payload.contenido or "").strip()
    if not contenido:
        raise HTTPException(status_code=400, detail="Contenido vacío")

    nuevo_comentario = Comentario(
        id_foro=foro_id,
        id_user=user.id_user,
        contenido=contenido,
        estado="activo",
        fecha_creacion=datetime.now()
    )
    try:
        db.add(nuevo_comentario)
        db.commit()
        db.refresh(nuevo_comentario)
    except Exception as e:
        try:
            db.rollback()
        except Exception:
            pass
        raise HTTPException(status_code=500, detail="Error guardando comentario")

    message = {
        "id_comentario": getattr(nuevo_comentario, 'id_comentario', None),
        "id_user": getattr(nuevo_comentario, 'id_user', None),
        "username": getattr(user, 'username', None),
        "contenido": nuevo_comentario.contenido,
        "fecha_creacion": str(nuevo_comentario.fecha_creacion)
    }

    # Notificar a conexiones WebSocket activas (no bloquear)
    try:
        await broadcast_message(foro_id, message)
    except Exception:
        # ignorar errores de notificación
        pass

    return message



