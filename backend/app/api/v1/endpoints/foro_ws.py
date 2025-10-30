from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.models import Comentario
from app.db.session import get_db
from datetime import datetime
import json

router = APIRouter(prefix="/ws/foro", tags=["Foro WS"])

active_connections = {}

async def connect_foro(websocket: WebSocket, foro_id: int):
    await websocket.accept()
    if foro_id not in active_connections:
        active_connections[foro_id] = []
    active_connections[foro_id].append(websocket)

async def disconnect_foro(websocket: WebSocket, foro_id: int):
    if foro_id in active_connections:
        active_connections[foro_id].remove(websocket)
        if not active_connections[foro_id]:
            del active_connections[foro_id]

async def broadcast_message(foro_id: int, message: dict):
    if foro_id in active_connections:
        for connection in active_connections[foro_id]:
            await connection.send_text(json.dumps(message))

@router.websocket("/{foro_id}")
async def foro_websocket(websocket: WebSocket, foro_id: int, db: Session = Depends(get_db)):
    await connect_foro(websocket, foro_id)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            # Crear el nuevo comentario
            nuevo_comentario = Comentario(
                foro_id=foro_id,
                id_user=payload["id_user"],
                contenido=payload["contenido"],
                estado="activo",
                fecha_creacion=datetime.now()
            )
            db.add(nuevo_comentario)
            db.commit()
            db.refresh(nuevo_comentario)

            message = {
                "id_comentario": nuevo_comentario.id_comentario,
                "id_user": nuevo_comentario.id_user,
                "contenido": nuevo_comentario.contenido,
                "fecha_creacion": str(nuevo_comentario.fecha_creacion)
            }

            await broadcast_message(foro_id, message)

    except WebSocketDisconnect:
        await disconnect_foro(websocket, foro_id)



