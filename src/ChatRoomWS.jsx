import { useEffect, useState, useRef, useCallback } from "react";
import "./chat.css";

export default function ChatRoomWS({ chatId, userId, onBack }) {
  const [messages, setMessages] = useState([]);
  const [content, setContent] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const connect = useCallback(() => {
    try {
      if (socketRef.current?.readyState === WebSocket.OPEN) {
        return; // Ya está conectado
      }
      
      socketRef.current = new WebSocket(`ws://localhost:8000/ws/chat/${chatId}`);

      socketRef.current.onopen = () => {
        console.log('WebSocket Connected');
        setIsConnected(true);
        // Limpiar cualquier timeout de reconexión pendiente
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current);
          reconnectTimeoutRef.current = null;
        }
      };

      socketRef.current.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        setMessages((prev) => [...prev, msg]);
      };

      socketRef.current.onerror = (error) => {
        console.error('WebSocket Error:', error);
        setIsConnected(false);
      };

      socketRef.current.onclose = (event) => {
        console.log('WebSocket Closed:', event.code, event.reason);
        setIsConnected(false);
        
        // Intentar reconectar después de 3 segundos
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('Intentando reconectar...');
          connect();
        }, 3000);
      };
    } catch (error) {
      console.error('Error al crear WebSocket:', error);
      setIsConnected(false);
    }
  }, [chatId]);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [chatId, connect]);


  const handleSend = () => {
    if (!content.trim() || !isConnected) return;
    
    try {
      socketRef.current.send(
        JSON.stringify({
          id_user: userId,
          contenido: content,
        })
      );
      setContent("");
    } catch (error) {
      console.error('Error al enviar mensaje:', error);
      // Intentar reconectar si hay un error al enviar
      connect();
    }
  };
  return (
    <>


      <div className="chatroom-panel">
        <button className="back-button" onClick={onBack}>&larr;</button>
        <h2 className="chatroom-title">Chat {chatId}</h2>
        <div className="messages-area">
          {messages.length === 0 ? (
            <div className="empty-state">No hay mensajes todavía</div>
          ) : (
            messages.map((msg) => (
              <div key={msg.id_mensaje} className="message">
                <div className="msg-avatar"><img src="/img/perfil.svg" alt="a"/></div>
                <div className="msg-body">
                  <div className="msg-author">Usuario {msg.id_user}</div>
                  <div className="msg-text">{msg.contenido}</div>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="chat-input-row">
          <input
            className="chat-input"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            onKeyDown={(e) => {
              // Enviar con Enter (sin Shift)
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="Enviar un mensaje..."
            aria-label="Escribe un mensaje"
          />
          <button className="chat-send" onClick={handleSend} title="Enviar">
            <img src="/img/graficos.svg" alt="send" />
          </button>
        </div>
      </div>
    </>
  );
}