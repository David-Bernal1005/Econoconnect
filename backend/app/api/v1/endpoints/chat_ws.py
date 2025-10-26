from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.chatmensaje import ChatMensaje
from sqlalchemy.sql import func

router = APIRouter()

# Diccionario global de conexiones activas
active_connections: dict[int, list[WebSocket]] = {}

async def connect(chat_id: int, websocket: WebSocket):
    await websocket.accept()
    if chat_id not in active_connections:
        active_connections[chat_id] = []
    active_connections[chat_id].append(websocket)

def disconnect(chat_id: int, websocket: WebSocket):
    if chat_id in active_connections:
        if websocket in active_connections[chat_id]:
            active_connections[chat_id].remove(websocket)

async def broadcast(chat_id: int, message: dict):
    for ws in active_connections.get(chat_id, []):  # 🔥 corregido aquí
        await ws.send_json(message)

@router.websocket("/ws/chat/{chat_id}")
async def chat_endpoint(websocket: WebSocket, chat_id: int, db: Session = Depends(get_db)):
    print(f"Nueva conexión WebSocket para chat {chat_id}")
    try:
        await connect(chat_id, websocket)
        print(f"Conexión establecida para chat {chat_id}")
        
        try:
            while True:
                data = await websocket.receive_json()
                print(f"Mensaje recibido en chat {chat_id}: {data}")

                # Guardar mensaje en la BD
                nuevo_mensaje = ChatMensaje(
                    id_chat=chat_id,
                    id_user=data["id_user"],
                    contenido=data["contenido"]
                )
                db.add(nuevo_mensaje)
                db.commit()
                db.refresh(nuevo_mensaje)

                # Reenviar mensaje a todos los usuarios conectados
                mensaje = {
                    "id_mensaje": nuevo_mensaje.id_mensaje,
                    "id_user": nuevo_mensaje.id_user,
                    "contenido": nuevo_mensaje.contenido,
                    "fecha_envio": str(nuevo_mensaje.fecha_envio)
                }
                print(f"Enviando mensaje a todos en chat {chat_id}: {mensaje}")
                await broadcast(chat_id, mensaje)
                
        except WebSocketDisconnect:
            print(f"Cliente desconectado del chat {chat_id}")
            disconnect(chat_id, websocket)
        except Exception as e:
            print(f"Error en el chat {chat_id}: {str(e)}")
            await websocket.close(code=1001)
    except Exception as e:
        print(f"Error al establecer conexión para chat {chat_id}: {str(e)}")
        try:
            await websocket.close(code=1001)
        except:
            pass
