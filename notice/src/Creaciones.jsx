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

  const allTags = [
    "Renta Variable",
    "Divisas",
    "Criptomonedas",
    "Noticias",
  ];

  const [selectedTags, setSelectedTags] = useState([...allTags]);
  const [mensaje, setMensaje] = useState("");
  const [noticias, setNoticias] = useState([]);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [editData, setEditData] = useState(null);
  const [loadingNoticias, setLoadingNoticias] = useState(false);

  // Cargar todas las noticias
  useEffect(() => {
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
    fetchNoticias();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

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
                  value={formData.soporte}
                  name="soporte"
                  onChange={e => setFormData(prev => ({ ...prev, soporte: e.target.value }))}
                />
              </div>
            </div>
            <div className="field">
              <label className="field-label">Etiquetas</label>
              <div className="tags">
                {allTags.map((t) => (
                  <button
                    key={t}
                    type="button"
                    className={`tag-pill ${selectedTags.includes(t) ? 'tag-active' : ''}`}
                    onClick={() => toggleTag(t)}
                  >
                    <span className="tag-x">×</span>
                    <span className="tag-text">{t}</span>
                  </button>
                ))}
              </div>
            </div>
            <div className="actions">
              {mensaje && <div className="mensaje">{mensaje}</div>}
              <button className="btn-publish" type="submit">Publicar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}