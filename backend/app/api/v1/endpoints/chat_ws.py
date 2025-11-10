from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from starlette.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.chatmensaje import ChatMensaje
from app.models.chat import Chat
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
    # Enviar en paralelo para que un cliente lento no bloquee a los demás
    tasks = []
    for ws in active_connections.get(chat_id, []):
        tasks.append(ws.send_json(message))
    if tasks:
        # gather sin esperar excepciones individuales
        import asyncio
        await asyncio.gather(*tasks, return_exceptions=True)

@router.websocket("/ws/chat/{chat_id}")
async def chat_endpoint(websocket: WebSocket, chat_id: int, db: Session = Depends(get_db)):
    print(f"Nueva conexión WebSocket para chat {chat_id}")
    try:
        await connect(chat_id, websocket)
        print(f"Conexión establecida para chat {chat_id}")
        # Enviar historial inicial (últimos 100 mensajes) empaquetado
        try:
            historial = db.query(ChatMensaje).filter(ChatMensaje.id_chat == chat_id).order_by(ChatMensaje.fecha_envio.asc()).limit(100).all()
            payload_hist = [
                {
                    "id_mensaje": m.id_mensaje,
                    "id_user": m.id_user,
                    "contenido": m.contenido,
                    "fecha_envio": str(m.fecha_envio)
                } for m in historial
            ]
            await websocket.send_json({"type": "history", "messages": payload_hist})
        except Exception as e:
            print(f"No se pudo cargar historial inicial de chat {chat_id}: {e}")
        
        try:
            while True:
                data = await websocket.receive_json()
                print(f"Mensaje recibido en chat {chat_id}: {data}")

                # Validar datos mínimos
                if not isinstance(data, dict) or not data.get("contenido") or not data.get("id_user"):
                    continue

                # Guardar mensaje en la BD
                # Persistir en threadpool para no bloquear el loop
                def _persist():
                    nuevo = ChatMensaje(
                        id_chat=chat_id,
                        id_user=data["id_user"],
                        contenido=data["contenido"].strip()
                    )
                    db.add(nuevo)
                    db.commit()
                    db.refresh(nuevo)
                    return nuevo
                nuevo_mensaje = await run_in_threadpool(_persist)

                # Reenviar mensaje a todos los usuarios conectados
                mensaje = {
                    "type": "message",
                    "id_mensaje": nuevo_mensaje.id_mensaje,
                    "id_user": nuevo_mensaje.id_user,
                    "contenido": nuevo_mensaje.contenido,
                    "fecha_envio": str(nuevo_mensaje.fecha_envio),
                    "client_id": data.get("client_id")  # para conciliar en cliente
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
