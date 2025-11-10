import { useEffect, useState, useRef, useCallback } from "react";
import "./chat.css";

export default function ChatRoomWS({ chat, userId, onBack }) {
  const [messages, setMessages] = useState([]);
  const [content, setContent] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [showInfo, setShowInfo] = useState(false);
  const [chatInfo, setChatInfo] = useState({ nombre: chat?.nombre || "", descripcion: chat?.descripcion || "" });
  const [addMemberUserId, setAddMemberUserId] = useState("");
  const [isAddingMember, setIsAddingMember] = useState(false);
  const [connectionError, setConnectionError] = useState("");
  const socketRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const messagesEndRef = useRef(null);
  const messagesAreaRef = useRef(null);
  const firstLoadRef = useRef(false);
  const chatId = chat?.id_chat;

  const API_BASE = 'http://127.0.0.1:8000';

  const connect = useCallback(() => {
    try {
      if (!chatId) return;
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
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current);
          reconnectTimeoutRef.current = null;
        }
      };

      socketRef.current.onmessage = (event) => {
        let payload;
        try { payload = JSON.parse(event.data); } catch { return; }
        if (payload?.type === 'history' && Array.isArray(payload.messages)) {
          // Reemplazar historial completo sólo si aún no hay mensajes (primera carga)
          setMessages(payload.messages);
          return;
        }
        if (payload?.type === 'message') {
          setMessages((prev) => {
            if (payload.client_id) {
              const idx = prev.findIndex(m => m.pending && m.client_id === payload.client_id);
              if (idx !== -1) {
                const copy = prev.slice();
                copy[idx] = { ...payload, pending: false };
                return copy;
              }
            }
            return [...prev, { ...payload, pending: false }];
          });
        }
      };

      socketRef.current.onerror = (error) => {
        console.error('WebSocket Error:', error);
        setIsConnected(false);
        setConnectionError("Error de conexión WebSocket. Verifica que el servidor esté corriendo en http://127.0.0.1:8000");
      };

      socketRef.current.onclose = (event) => {
        console.log('WebSocket Closed:', event.code, event.reason);
        setIsConnected(false);
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
  }, [chatId, API_BASE]);

  // Auto-scroll al final: en la primera carga saltamos directo al final;
  // luego, solo si el usuario está cerca del final (comportamiento tipo foro)
  useEffect(() => {
    if (!messagesAreaRef.current) return;
    const el = messagesAreaRef.current;
    if (firstLoadRef.current) {
      // primera carga: ir al final sin animación
      el.scrollTop = el.scrollHeight;
      firstLoadRef.current = false;
      return;
    }
    const nearBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 120;
    if (nearBottom) el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  // Al cambiar de chat, reseteamos info visible y mensajes
  useEffect(() => {
    setShowInfo(false);
    setMessages([]);
    firstLoadRef.current = true; // en cada cambio de chat, empezar desde el último
    setChatInfo({
      nombre: chat?.nombre || (chatId ? `Chat ${chatId}` : ""),
      descripcion: chat?.descripcion || "",
    });
  }, [chatId, chat?.nombre, chat?.descripcion]);

  useEffect(() => {
    connect();
    checkAdminStatus();
    // Cargar nombre y descripción del grupo correctamente
    (async () => {
      if (!chatId) return;
      const token = localStorage.getItem('token');
      const authHeaders = token ? { 'Authorization': `Bearer ${token}` } : {};
      try {
        // Endpoint directo por id
        const oneResp = await fetch(`${API_BASE}/api/v1/grupos/${chatId}`, { headers: authHeaders });
        if (oneResp.ok) {
          const g = await oneResp.json();
          setChatInfo({
            nombre: g?.nombre || (chatId ? `Chat ${chatId}` : ""),
            descripcion: g?.descripcion || "",
          });
        } else {
          // Fallback a listas si el endpoint directo no está disponible
          let found = null;
          const misResp = await fetch(`${API_BASE}/api/v1/grupos/mis-grupos/`, { headers: authHeaders });
          if (misResp.ok) {
            const list = await misResp.json();
            found = Array.isArray(list) ? list.find(c => c.id_chat === Number(chatId)) : null;
          }
          if (!found) {
            const pubResp = await fetch(`${API_BASE}/api/v1/grupos/publicos/`);
            if (pubResp.ok) {
              const listPub = await pubResp.json();
              found = Array.isArray(listPub) ? listPub.find(c => c.id_chat === Number(chatId)) : null;
            }
          }
          if (found) {
            setChatInfo({
              nombre: found.nombre || (chatId ? `Chat ${chatId}` : ""),
              descripcion: found.descripcion || "",
            });
          } else {
            setChatInfo({ nombre: chat?.nombre || (chatId ? `Chat ${chatId}` : ""), descripcion: chat?.descripcion || "" });
          }
        }
      } catch (err) {
        console.warn('No se pudo cargar info del chat:', err);
      setChatInfo({ nombre: chat?.nombre || (chatId ? `Chat ${chatId}` : ""), descripcion: chat?.descripcion || "" });
      }
    })();

    // Cargar historial desde la BD
    (async () => {
      if (!chatId) return;
      try {
        const res = await fetch(`${API_BASE}/api/v1/chats/${chatId}/mensajes?limit=200`);
        if (res.ok) {
          const hist = await res.json();
          if (Array.isArray(hist)) {
            setMessages(hist);
          }
        }
      } catch (e) {
        console.warn('No se pudo cargar el historial de mensajes', e);
      }
    })();

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
    if (!content.trim() || !isConnected || !chatId) return;
    try {
      const clientId = (crypto?.randomUUID?.() || `${Date.now()}-${Math.random().toString(16).slice(2)}`);
      const sending = content;

      // Optimistic UI: agregar mensaje "pendiente" al instante
      const tempMsg = {
        id_mensaje: `tmp-${clientId}`,
        id_user: userId,
        contenido: sending,
        fecha_envio: new Date().toISOString(),
        client_id: clientId,
        pending: true,
        type: 'message',
      };
      setMessages((prev) => [...prev, tempMsg]);

      // Enviar al servidor con client_id para conciliar
      socketRef.current.send(
        JSON.stringify({ id_user: userId, contenido: sending, client_id: clientId })
      );
      setContent("");
    } catch (error) {
      console.error('Error al enviar mensaje:', error);
      connect();
    }
  };

  return (
    <>
      <div className="chatroom-panel">
        <div className="chat-header">
          <button className="back-button" onClick={onBack}>&larr;</button>
          <h2
            className="chatroom-title"
            onClick={() => setShowInfo((v) => !v)}
            title={showInfo ? 'Ocultar descripción' : 'Mostrar descripción'}
          >
            {chatInfo.nombre || `Chat ${chatId}`}
          </h2>
          <div style={{ fontSize: 12, color: isConnected ? 'green' : 'red' }}>
            {isConnected ? '🟢 Conectado' : '🔴 Desconectado'}
          </div>
        </div>

        {showInfo && (
          <div className="chat-subheader">
            <div className="chat-subtitle">Información del chat</div>
            <div className="chat-desc">
              {chatInfo.descripcion?.trim() ? chatInfo.descripcion : 'Sin descripción'}
            </div>
          </div>
        )}

        {connectionError && (
          <div style={{ padding: 8, backgroundColor: '#ffcccc', color: '#cc0000', marginBottom: 8, borderRadius: 4 }}>
            {connectionError}
          </div>
        )}

  <div className="messages-area whatsapp-bg" ref={messagesAreaRef}>
          {messages.length === 0 && (
            <div className="empty-state">No hay mensajes todavía</div>
          )}
          {messages.map((msg) => {
            const isMine = msg.id_user === userId;
            return (
              <div
                key={msg.id_mensaje || `${msg.id_user}-${Math.random()}`}
                className={`message-bubble ${isMine ? 'mine' : 'other'} ${msg.pending ? 'pending' : ''}`}
              >
                {!isMine && (
                  <div className="bubble-author">Usuario {msg.id_user}</div>
                )}
                <div className="bubble-text">{msg.contenido}</div>
                {msg.pending ? (
                  <div className="bubble-meta">Enviando…</div>
                ) : msg.fecha_envio && (
                  <div className="bubble-meta">
                    {new Date(msg.fecha_envio).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                )}
              </div>
            );
          })}
          <div ref={messagesEndRef} />
        </div>

        <div className="composer">
          <input
            className="composer-input"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="Mensaje"
            disabled={!isConnected}
          />
          <button
            className="composer-send"
            onClick={handleSend}
            disabled={!isConnected || !content.trim()}
          >
            ▶
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
