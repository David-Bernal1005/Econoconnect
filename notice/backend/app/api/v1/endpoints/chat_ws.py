from fastapi import APIRouter, WebSocket , WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.chatmensaje import ChatMensaje
from sqlalchemy.sql import func

router = APIRouter()
active_connections: dict[int, list[WebSocket]] = {}

async def connect(chat_id: int, websocket: WebSocket):
    await websocket.accept()
    if chat_id not in active_connections:
        active_connections[chat_id] = []
    active_connections[chat_id].append(websocket)
    
def disconnect(chat_id: int, websocket: WebSocket):
    active_connections[chat_id].remove(websocket)

async def broadcast(chat_id: int, message: dict):
    for ws in active_connections.get_db(chat_id, []):
        await ws.send_json(message)
        
@router.websocket("/ws/chat/{chat_id}")
async def chat_endpoint(websocket: WebSocket, chat_id: int, db: Session = Depends(get_db)):
    await connect(chat_id,websocket)
    try:
        while True:
            data = await websocket.receive_json()
            nuevo_mensaje = ChatMensaje(
                id_chat = chat_id,
                id_user = data["id_user"],
                contenido = data["contenido"]
            )
            db.add(nuevo_mensaje)
            db.commit()
            db.refresh(nuevo_mensaje)
            
            await broadcast(chat_id, {
                "id_mensaje": nuevo_mensaje.id_mensaje,
                "id_user": nuevo_mensaje.id_user,
                "contenido": nuevo_mensaje.contenido,
                "fecha_envio": str(nuevo_mensaje.fecha_envio)
            })
    except WebSocketDisconnect:
        disconnect(chat_id,websocket)