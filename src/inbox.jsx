import { useEffect, useState, useCallback } from "react";
import "./inbox.css";

export default function Inbox({ userId, onSelectChat }) {
  const [chats, setChats] = useState([]);
  const [showCreate, setShowCreate] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [groupForm, setGroupForm] = useState({
    nombre: "",
    descripcion: "",
    tipo: "grupo",
    visibilidad: "publico",
  });
  const maxNameLength = 50;
  const maxDescLength = 300;
  const API_BASE = "http://127.0.0.1:8000";

  const refreshChats = async () => {
    try {
      const baseList = await fetch(`${API_BASE}/api/v1/chats/${userId}`).then(r => r.ok ? r.json() : []);
      const pubList = await fetch(`${API_BASE}/api/v1/grupos/publicos/`).then(r => r.ok ? r.json() : []);
      // Merge descripcion from public groups when IDs match
      const pubMap = new Map(pubList.map(g => [g.id_chat, g]));
      const merged = (Array.isArray(baseList) ? baseList : []).map(item => {
        const pub = pubMap.get(item.id_chat);
        return pub ? { ...item, descripcion: pub.descripcion, nombre: item.nombre || pub.nombre } : item;
      });
      setChats(merged);
    } catch (e) {
      setChats([]);
    }
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

  const validate = useCallback((data) => {
    const vErrors = {};
    if (!data.nombre.trim()) {
      vErrors.nombre = "El nombre es requerido";
    } else if (data.nombre.trim().length > maxNameLength) {
      vErrors.nombre = `Máx ${maxNameLength} caracteres`;
    }
    if (data.descripcion && data.descripcion.length > maxDescLength) {
      vErrors.descripcion = `Máx ${maxDescLength} caracteres`;
    }
    return vErrors;
  }, [maxNameLength, maxDescLength]);

  useEffect(() => {
    setErrors(validate(groupForm));
  }, [groupForm, validate]);

  const handleChange = (field, value) => {
    setGroupForm((prev) => ({ ...prev, [field]: value }));
  };

  const markTouched = (field) => setTouched((t) => ({ ...t, [field]: true }));

  const canSubmit = Object.keys(errors).length === 0 && groupForm.nombre.trim() && !submitting;

  const handleCreateGroup = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const currentErrors = validate(groupForm);
      setErrors(currentErrors);
      if (Object.keys(currentErrors).length) {
        return;
      }
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
        let detail = "Error al crear el chat/grupo";
        try { const err = await res.json(); detail = err.detail || detail; } catch {}
        throw new Error(detail);
      }
      await res.json();
      setShowCreate(false);
      setGroupForm({ nombre: "", descripcion: "", tipo: "grupo", visibilidad: "publico" });
      setTouched({});
      refreshChats();
    } catch (err) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  // Cerrar panel con Escape
  useEffect(() => {
    const onKey = (e) => {
      if (e.key === "Escape" && showCreate) setShowCreate(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [showCreate]);

  return (
    <div className="box">
      <h2 className="box-title">📩 Chats</h2>

      <div className="create-toggle-row">
        <button
          className={"inbox-button create-toggle" + (showCreate ? " active" : "")}
          onClick={() => setShowCreate((v) => !v)}
          aria-expanded={showCreate}
        >
          {showCreate ? "Cerrar creación" : "＋ Crear Chat / Grupo"}
        </button>
      </div>

      <div className={"create-group-wrapper" + (showCreate ? " open" : "")}>
        <div className="create-group-form" aria-hidden={!showCreate}>
          <form onSubmit={handleCreateGroup} noValidate>
            <div className="form-group">
              <label className="form-label">Nombre</label>
              <input
                type="text"
                placeholder="Nombre del chat"
                value={groupForm.nombre}
                maxLength={maxNameLength + 5} /* buffer visual */
                onBlur={() => markTouched("nombre")}
                onChange={(e) => handleChange("nombre", e.target.value)}
                required
              />
              <div className="field-meta-row">
                <small className="counter" aria-live="polite">
                  {groupForm.nombre.trim().length}/{maxNameLength}
                </small>
                {touched.nombre && errors.nombre && (
                  <small className="error-text">{errors.nombre}</small>
                )}
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">Descripción <span className="optional">(opcional)</span></label>
              <textarea
                placeholder="Describe el propósito de este grupo"
                value={groupForm.descripcion}
                maxLength={maxDescLength + 10}
                onBlur={() => markTouched("descripcion")}
                onChange={(e) => handleChange("descripcion", e.target.value)}
              />
              <div className="field-meta-row">
                <small className="counter" aria-live="polite">
                  {groupForm.descripcion.length}/{maxDescLength}
                </small>
                {touched.descripcion && errors.descripcion && (
                  <small className="error-text">{errors.descripcion}</small>
                )}
              </div>
            </div>
            <div className="form-group">
              <label className="form-label">Visibilidad</label>
              <select
                value={groupForm.visibilidad}
                onChange={(e) => handleChange("visibilidad", e.target.value)}
                disabled={!isAdmin}
              >
                <option value="publico">Público</option>
                {isAdmin && <option value="privado">Privado</option>}
              </select>
              {!isAdmin && (
                <small className="helper-text">Solo administradores pueden crear grupos privados</small>
              )}
            </div>
            <div className="actions-row">
              <button
                type="submit"
                className="create-group-submit"
                disabled={!canSubmit}
              >
                {submitting ? "Creando..." : "Crear"}
              </button>
              {Object.keys(errors).length > 0 && (
                <small className="error-global" aria-live="assertive">
                  Corrige los campos marcados
                </small>
              )}
            </div>
          </form>
        </div>
      </div>

      <ul className="inbox-list" aria-label="Lista de chats">
        {chats.map((chat) => (
          <li key={chat.id_chat} className="inbox-item">
            <button className="inbox-button" onClick={() => onSelectChat(chat)}>
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
