// Creaciones.jsx
import React, { useState, useEffect } from "react";
import "./Creaciones.css";
import Menu from "./Menu";
import MisNoticias from "./MisNoticias";

export default function Creaciones() {
  const [misNoticiasOpen, setMisNoticiasOpen] = useState(false);
  // Obtener el usuario desde el login
  const usuarioActual = localStorage.getItem("nombre_usuario") || "";

  const [formData, setFormData] = useState({
    titulo: "",
    descripcion: "",
    soporte: "",
  });

  const [allTags, setAllTags] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);
  const [mensaje, setMensaje] = useState("");
  const [noticias, setNoticias] = useState([]);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [editData, setEditData] = useState(null);
  const [loadingNoticias, setLoadingNoticias] = useState(false);

  // Cargar categorías y noticias
  useEffect(() => {
    async function fetchCategorias() {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/v1/categorias");
        const data = await res.json();
        let tags = Array.isArray(data) ? data.map(cat => cat.Nombre_Categoria) : [];
        // Fallback si la API no responde o no hay categorías
        if (!tags.length) {
          tags = ["Renta Variable", "Divisas", "Criptomonedas", "Noticias"];
        }
        setAllTags(tags);
        setSelectedTags(prev => prev.length === 0 ? tags : prev);
      } catch (err) {
        const tags = ["Renta Variable", "Divisas", "Criptomonedas", "Noticias"];
        setAllTags(tags);
        setSelectedTags(tags);
      }
    }
    async function fetchNoticias() {
      setLoadingNoticias(true);
      try {
        const res = await fetch("http://127.0.0.1:8000/api/v1/noticias");
        const data = await res.json();
        setNoticias(Array.isArray(data) ? data : []);
      } catch (err) {
        setNoticias([]);
      }
      setLoadingNoticias(false);
    }
    fetchCategorias();
    fetchNoticias();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

      // Filtrar noticias por etiquetas seleccionadas (solo las que existen en la tabla categorias y están seleccionadas)
      const activeTags = allTags.filter(t => selectedTags.includes(t));
      const noticiasFiltradas = noticias.filter(n => activeTags.includes(n.categoria || n.Categoria || n.Nombre_Categoria));
  const toggleTag = (tag) => {
    setSelectedTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const categoria = selectedTags.length > 0 ? selectedTags[0] : "";
    if (!usuarioActual) {
      setMensaje("Debes iniciar sesión para crear noticias.");
  setTimeout(() => setMensaje(""), 4000);
      return;
    }
    const noticiaPayload = {
      titulo: formData.titulo,
      resumen: formData.descripcion,
      enlace: formData.soporte,
      fecha_publicacion: new Date().toISOString(),
      categoria: categoria,
      usuario: usuarioActual
    };
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/noticias", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(noticiaPayload)
      });
      if (res.ok) {
        setMensaje("¡Noticia creada!");
        setFormData({ titulo: "", descripcion: "", soporte: "" });
        // Recargar noticias
        fetch("http://127.0.0.1:8000/api/v1/noticias")
          .then(res => res.json())
          .then(data => setNoticias(Array.isArray(data) ? data : []));
      } else {
        setMensaje("Error al guardar la noticia");
      }
      setTimeout(() => setMensaje(""), 4000);
    } catch (err) {
      setMensaje("Error de red: " + err.message);
      console.error("Error de red:", err);
    }
  };

  const handleEditClick = (noticia) => {
    setEditData({ ...noticia });
    setEditModalOpen(true);
  };

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditData(prev => ({ ...prev, [name]: value }));
  };

  const handleEditSave = async () => {
    if (!editData) return;
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/noticias/${editData.Id_Noticia}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          titulo: editData.titulo,
          resumen: editData.resumen,
          enlace: editData.enlace,
          Id_Categoria: editData.Id_Categoria,
          Id_Fuente: editData.Id_Fuente,
          activa: editData.activa
        })
      });
      if (res.ok) {
        setMensaje("Noticia actualizada");
        setEditModalOpen(false);
        setEditData(null);
        // Recargar noticias
        fetch("http://127.0.0.1:8000/api/v1/noticias")
          .then(res => res.json())
          .then(data => setNoticias(Array.isArray(data) ? data : []));
      } else {
        setMensaje("Error al actualizar");
      }
    } catch (err) {
      setMensaje("Error de red: " + err.message);
    }
    setTimeout(() => setMensaje(""), 4000);
  };

  const handleInactivar = async (noticiaId) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/noticias/${noticiaId}/inactivar`, {
        method: "PATCH"
      });
      if (res.ok) {
        setMensaje("Noticia inactivada");
        // Recargar noticias
        fetch("http://127.0.0.1:8000/api/v1/noticias")
          .then(res => res.json())
          .then(data => setNoticias(Array.isArray(data) ? data : []));
      } else {
        setMensaje("Error al inactivar");
      }
    } catch (err) {
      setMensaje("Error de red: " + err.message);
    }
    setTimeout(() => setMensaje(""), 4000);
  };

  // Filtrar noticias por etiquetas seleccionadas
  // Eliminada declaración duplicada de noticiasFiltradas

  return (
    <div className="creaciones-root">
      <div className="creaciones-layout">
        <aside className="creaciones-menu">
          <Menu />
        </aside>
        <div className="creaciones-container">
          <a
            href="/misnoticias"
            target="_blank"
            rel="noopener noreferrer"
            className="mis-noticias-btn"
          >
            Ver y editar mis noticias
          </a>
          <header className="creaciones-header">
            <div className="brand-pill">Creaciones</div>
          </header>
          <form className="creaciones-form" onSubmit={handleSubmit}>
            <div className="field">
              <label className="field-label">Título</label>
              <input
                className="input-title"
                name="titulo"
                value={formData.titulo}
                onChange={handleChange}
                placeholder="Escribe el título..."
              />
            </div>
            <div className="field">
              <label className="field-label">Descripción</label>
              <textarea
                className="textarea-desc"
                name="descripcion"
                value={formData.descripcion}
                onChange={handleChange}
                placeholder="Escribe la descripción..."
              />
            </div>
            <div className="field">
              <label className="field-label">Soporte</label>
              <div className="support-row">
                <input
                  type="url"
                  className="input-title"
                  placeholder="Pega aquí la URL de soporte"
                  name="soporte"
                  value={formData.soporte}
                  onChange={handleChange}
                />
              </div>
            </div>
            <div className="field">
              <label className="field-label">Etiquetas</label>
              <div className="tags">
                {allTags.length === 0 ? (
                  <span style={{ color: '#fff', fontWeight: 'bold' }}>No hay etiquetas disponibles</span>
                ) : (
                  allTags.map((t) => (
                    <button
                      key={t}
                      type="button"
                      className={`tag-pill ${selectedTags.includes(t) ? 'tag-active' : ''}`}
                      onClick={() => toggleTag(t)}
                      style={{ cursor: 'pointer', margin: '0 8px 8px 0', fontWeight: 'bold', fontSize: '18px', padding: '12px 32px', background: selectedTags.includes(t) ? '#f1c40f' : '#555a62', color: selectedTags.includes(t) ? '#232627' : '#fff', border: 'none', borderRadius: '22px', transition: 'background 0.2s' }}
                    >
                      <span className="tag-x">×</span>
                      <span className="tag-text">{t}</span>
                    </button>
                  ))
                )}
              </div>
            </div>
            <div className="actions">
              {mensaje && <div className="mensaje">{mensaje}</div>}
              <button className="btn-publish" type="submit">Publicar</button>
            </div>
          </form>
          {/* Mostrar noticias filtradas por etiquetas seleccionadas */}
          <div className="noticias-list">
            {noticiasFiltradas.map((n, idx) => (
              <div key={idx} className="news-container">
                <h3>{n.titulo}</h3>
                <p>{n.resumen}</p>
                {n.enlace && <a href={n.enlace} target="_blank" rel="noopener noreferrer">{n.enlace}</a>}
                <div style={{ fontSize: '0.9rem', color: '#f1c40f', marginTop: 8 }}>{n.categoria || n.Categoria || n.Nombre_Categoria}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}