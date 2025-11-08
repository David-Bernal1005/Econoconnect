import { useEffect, useState, useRef, useCallback } from "react";
import "./chat.css";

export default function ChatRoomWS({ chatId, userId, onBack }) {
  const [messages, setMessages] = useState([]);
  const [content, setContent] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const [showCreateGroup, setShowCreateGroup] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [groupForm, setGroupForm] = useState({
    nombre: '',
    descripcion: '',
    visibilidad: 'publico'
  });
  const socketRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const API_BASE = 'http://127.0.0.1:8000';

  const connect = useCallback(() => {
    try {
      if (socketRef.current?.readyState === WebSocket.OPEN) {
        return; // Ya está conectado
      }
      
  socketRef.current = new WebSocket(`${API_BASE.replace('http', 'ws')}/ws/chat/${chatId}`);

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
    const response = await fetch(`${API_BASE}/api/v1/user/roles`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const data = await response.json();
    setIsAdmin(data.rol === 'administrador');
  } catch (error) {
    console.error('Error al verificar rol:', error);
  }
  };

  const handleCreateGroup = async (e) => {
    e.preventDefault();
    try {
        const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE}/api/v1/grupos/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(groupForm)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error al crear el grupo');
        }

        const nuevoGrupo = await response.json();
        setShowCreateGroup(false);
        setGroupForm({
            nombre: '',
            descripcion: '',
            visibilidad: 'publico'
        });
        
        // Aquí puedes añadir lógica para cambiar al nuevo grupo
        if (typeof onBack === 'function') {
            onBack(); // Para actualizar la lista de chats
        }
    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
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
          <button 
            className="create-group-button" 
            onClick={() => setShowCreateGroup(!showCreateGroup)}
          >
            {showCreateGroup ? 'Cancelar' : 'Crear Grupo'}
          </button>
        </div>

        {showCreateGroup && (
          <div className="create-group-form">
            <form onSubmit={handleCreateGroup}>
              <div className="form-group">
                <input
                  type="text"
                  placeholder="Nombre del grupo"
                  value={groupForm.nombre}
                  onChange={(e) => setGroupForm({...groupForm, nombre: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <textarea
                  placeholder="Descripción del grupo"
                  value={groupForm.descripcion}
                  onChange={(e) => setGroupForm({...groupForm, descripcion: e.target.value})}
                />
              </div>
              <div className="form-group">
                <select
                  value={groupForm.visibilidad}
                  onChange={(e) => setGroupForm({...groupForm, visibilidad: e.target.value})}
                  disabled={!isAdmin}
                >
                  <option value="publico">Público</option>
                  {isAdmin && <option value="privado">Privado</option>}
                </select>
              </div>
              <button type="submit" className="create-group-submit">
                Crear Grupo
              </button>
            </form>
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
          />
          <button className="chat-send" onClick={handleSend} title="Enviar">
            <img src="/img/graficos.svg" alt="send" />
          </button>
        </div>
      </div>
    </>
  );
}