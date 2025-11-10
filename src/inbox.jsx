import { useEffect, useState } from "react";
import "./inbox.css";

export default function Inbox({ userId, onSelectChat }) {
  const [chats, setChats] = useState([]);
  const [showCreate, setShowCreate] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [groupForm, setGroupForm] = useState({
    nombre: "",
    descripcion: "",
    tipo: "grupo",
    visibilidad: "publico",
    // Agregar cualquier otro campo requerido por el backend
    creador_id: userId, // Asegurarse de que el ID del creador se envíe
  });
  const API_BASE = "http://127.0.0.1:8000";

  const refreshChats = () => {
    fetch(`${API_BASE}/api/v1/chats/${userId}`)
      .then((res) => res.json())
      .then(setChats)
      .catch(() => setChats([]));
  };

  useEffect(() => {
    refreshChats();
  }, [userId]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    console.log("Token en localStorage:", token ? "Existe" : "No existe");
    console.log("Token valor:", token);
    
    if (!token) {
      console.warn("No hay token en localStorage");
      setIsAdmin(false);
      return;
    }

    fetch(`${API_BASE}/api/v1/user/roles`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => {
        console.log("Response status:", r.status);
        if (!r.ok) {
          throw new Error(`HTTP ${r.status}: No autorizado`);
        }
        return r.json();
      })
      .then((data) => {
        console.log("Rol data:", data);
        const raw = data?.rol?.toString().toLowerCase() || "";
        console.log("Rol normalizado:", raw);
        // Verificar cualquier variante que incluya "administrador"
        setIsAdmin(raw.includes("administrador"));
        console.log("¿Es admin?:", raw.includes("administrador"));
      })
      .catch((err) => {
        console.error("Error al obtener rol:", err);
        setIsAdmin(false);
      });
  }, []);

  const handleCreateGroup = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      
      if (!token) {
        throw new Error("No hay token de autenticación");
      }

      // Validar que solo los administradores puedan crear grupos privados
      if (groupForm.visibilidad === "privado" && !isAdmin) {
        throw new Error("Solo los administradores pueden crear grupos privados");
      }

      // Verificar el estado de autenticación
      try {
        // Verificar el rol primero
        const roleCheck = await fetch(`${API_BASE}/api/v1/user/roles`, {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });
        const roleData = await roleCheck.json();
        console.log("Verificación de rol:", roleData);
      } catch (error) {
        console.error("Error al verificar rol:", error);
      }

      // Construir el objeto de datos para enviar
      const dataToSend = {
        nombre: groupForm.nombre,
        descripcion: groupForm.descripcion,
        visibilidad: groupForm.visibilidad.toLowerCase(),
        tipo: "grupo"
      };
      
      console.log("Intentando crear grupo con:", {
        datos: dataToSend,
        token: token.substring(0, 20) + "...", // Solo mostrar parte del token por seguridad
        esAdmin: isAdmin
      });

      // Debug de la información que se enviará
      console.log('Token:', token);
      console.log('Datos a enviar:', dataToSend);
      console.log('Headers:', {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      });

      const res = await fetch(`${API_BASE}/api/v1/grupos/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
          "Accept": "application/json",
          "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify(dataToSend)
      });
      if (!res.ok) {
        let errorMessage;
        try {
          const err = await res.json();
          console.error('Error del servidor:', {
            status: res.status,
            statusText: res.statusText,
            error: err,
            headers: Object.fromEntries(res.headers.entries()),
            url: res.url,
            type: res.type
          });
          
          // Mostrar información más detallada del error
          console.error('Detalles completos de la respuesta:', {
            status: res.status,
            ok: res.ok,
            redirected: res.redirected,
            type: res.type,
            url: res.url
          });
          
          errorMessage = err.detail || err.message || `Error ${res.status}: No autorizado - ${JSON.stringify(err)}`;
        } catch (e) {
          console.error('Error al parsear respuesta:', e);
          errorMessage = `Error ${res.status}: ${res.statusText}`;
        }
        throw new Error(errorMessage);
      }
      const responseData = await res.json();
      console.log('Respuesta exitosa:', responseData);
      setShowCreate(false);
      setGroupForm({ nombre: "", descripcion: "", tipo: "grupo", visibilidad: "publico" });
      refreshChats();
      alert("Chat/Grupo creado exitosamente");
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="box">
      <h2 className="box-title">📩 Chats</h2>

      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <button className="inbox-button" onClick={() => setShowCreate((v) => !v)}>
          {showCreate ? "Cancelar" : "Crear Chat/Grupo"}
        </button>
      </div>

      {showCreate && (
        <div className="create-group-form" style={{ padding: 8 }}>
          <form onSubmit={handleCreateGroup}>
            <div className="form-group">
              <input
                type="text"
                placeholder="Nombre"
                value={groupForm.nombre}
                onChange={(e) => setGroupForm({ ...groupForm, nombre: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <textarea
                placeholder="Descripción"
                value={groupForm.descripcion}
                onChange={(e) => setGroupForm({ ...groupForm, descripcion: e.target.value })}
              />
            </div>
            <div className="form-group">
              <select
                value={groupForm.visibilidad}
                onChange={(e) => {
                  console.log('Cambiando visibilidad a:', e.target.value);
                  setGroupForm({ ...groupForm, visibilidad: e.target.value });
                }}
                disabled={!isAdmin}
              >
                <option value="publico">Público</option>
                {isAdmin && <option value="privado">Privado</option>}
              </select>
              <div style={{ marginTop: '4px', fontSize: '12px', color: 'gray' }}>
                Estado actual: {isAdmin ? 'Eres administrador' : 'No eres administrador'}
              </div>
              {!isAdmin && <small style={{ color: "gray", marginTop: 4 }}>Solo administradores pueden crear grupos privados</small>}
            </div>
            <button type="submit" className="create-group-submit">Crear</button>
          </form>
        </div>
      )}

      <ul className="inbox-list">
        {chats.map((chat) => (
          <li key={chat.id_chat} className="inbox-item">
            <button className="inbox-button" onClick={() => onSelectChat(chat.id_chat)}>
              <div className="avatar">
                <img src="/img/perfil.svg" alt="avatar" />
              </div>
              <div className="inbox-meta">
                <div className="inbox-name">{chat.nombre}</div>
                <div className="inbox-last">{chat.ultimo_mensaje || "Sin mensajes"}</div>
              </div>
            </button>
          </li>
        ))}
      </ul>

    </div>
  );
}
