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
        const raw = (data?.rol ?? data?.role ?? (Array.isArray(data?.roles) ? data.roles[0] : ""))
          ?.toString()
          .toLowerCase();
        console.log("Rol normalizado:", raw);
        setIsAdmin(raw === "administrador" || raw === "admin");
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
      const res = await fetch(`${API_BASE}/api/v1/grupos/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(groupForm),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Error al crear el chat/grupo");
      }
      await res.json();
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
                onChange={(e) => setGroupForm({ ...groupForm, visibilidad: e.target.value })}
                disabled={!isAdmin}
              >
                <option value="publico">Público</option>
                {isAdmin && <option value="privado">Privado</option>}
              </select>
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
