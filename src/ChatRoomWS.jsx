import { useEffect, useState, useRef, useCallback } from "react";
import "./chat.css";

export default function ChatRoomWS({ chatId, userId, onBack }) {
  const [messages, setMessages] = useState([]);
  const [content, setContent] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [addMemberUserId, setAddMemberUserId] = useState("");
  const [isAddingMember, setIsAddingMember] = useState(false);
  const [connectionError, setConnectionError] = useState("");
  const socketRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const processedMessagesRef = useRef(new Set());

  const API_BASE = 'http://127.0.0.1:8000';

  const connect = useCallback(() => {
    try {
      if (socketRef.current?.readyState === WebSocket.OPEN) {
        return; // Ya está conectado
      }
      
      const wsUrl = `${API_BASE.replace('http', 'ws')}/ws/chat/${chatId}`;
      console.log('Intentando conectar a:', wsUrl);
      socketRef.current = new WebSocket(wsUrl);

      socketRef.current.onopen = () => {
        console.log('WebSocket Connected');
        setIsConnected(true);
        setConnectionError("");
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
        setConnectionError("Error de conexión WebSocket. Verifica que el servidor esté corriendo en http://127.0.0.1:8000");
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
      setConnectionError("Error al crear la conexión WebSocket");
    }
  }, [chatId]);

  useEffect(() => {
    connect();
    checkAdminStatus();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [chatId, connect]);

  const checkAdminStatus = async () => {
    try {
      const token = localStorage.getItem('token');
      console.log("Token en localStorage:", token ? "Existe" : "No existe");
      console.log("Token valor:", token);
      
      if (!token) {
        console.warn("No hay token en localStorage");
        setIsAdmin(false);
        return;
      }

      const response = await fetch(`${API_BASE}/api/v1/user/roles`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      console.log("Response status:", response.status);
      
      if (!response.ok) {
        console.error("Error al obtener rol, status:", response.status);
        const errorData = await response.json().catch(() => ({}));
        console.error("Error detail:", errorData);
        setIsAdmin(false);
        return;
      }

      const data = await response.json();
      console.log("Rol data:", data);
      
      const raw = (data?.rol ?? data?.role ?? (Array.isArray(data?.roles) ? data.roles[0] : ""))
        ?.toString()
        .toLowerCase();
      console.log("Rol normalizado:", raw);
      
      setIsAdmin(raw === 'administrador' || raw === 'admin');
    } catch (error) {
      console.error('Error al verificar rol:', error);
      setIsAdmin(false);
    }
  };

  const handleAddMember = async (e) => {
    e.preventDefault();
    if (!addMemberUserId) return;
    try {
      setIsAddingMember(true);
      const token = localStorage.getItem('token');
      const res = await fetch(`${API_BASE}/api/v1/chatmiembros/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          id_chat: Number(chatId),
          id_user: Number(addMemberUserId),
          rol_chat: 'miembro'
        })
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'No se pudo agregar el usuario al grupo');
      }
      setAddMemberUserId("");
      alert('Usuario agregado al grupo');
    } catch (err) {
      alert(err.message);
    } finally {
      setIsAddingMember(false);
    }
  };

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
        <div className="chat-header">
          <button className="back-button" onClick={onBack}>&larr;</button>
          <h2 className="chatroom-title">Chat {chatId}</h2>
          <div style={{ fontSize: 12, color: isConnected ? 'green' : 'red' }}>
            {isConnected ? '🟢 Conectado' : '🔴 Desconectado'}
          </div>
        </div>

        {connectionError && (
          <div style={{ padding: 8, backgroundColor: '#ffcccc', color: '#cc0000', marginBottom: 8, borderRadius: 4 }}>
            {connectionError}
          </div>
        )}

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
            disabled={!isConnected}
          />
          <button className="chat-send" onClick={handleSend} title="Enviar" disabled={!isConnected}>
            <img src="/img/graficos.svg" alt="send" />
          </button>
        </div>

        {isAdmin && (
          <div className="add-member-panel" style={{ marginTop: 12, padding: 8, backgroundColor: '#f0f0f0', borderRadius: 4 }}>
            <form onSubmit={handleAddMember} style={{ display: 'flex', gap: 8 }}>
              <input
                type="number"
                min="1"
                placeholder="ID de usuario a agregar"
                value={addMemberUserId}
                onChange={(e) => setAddMemberUserId(e.target.value)}
                required
              />
              <button type="submit" disabled={isAddingMember}>
                {isAddingMember ? 'Agregando...' : 'Agregar miembro'}
              </button>
            </form>
          </div>
        )}
      </div>
    </>
  );
}
