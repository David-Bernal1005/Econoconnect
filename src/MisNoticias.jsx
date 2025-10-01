
import React, { useState, useEffect } from "react";
import Menu from "./Menu";

export default function MisNoticias() {
  const usuarioActual = localStorage.getItem("nombre_usuario") || "";
  const [noticias, setNoticias] = useState([]);
  const [mensaje, setMensaje] = useState("");
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [editData, setEditData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchNoticias() {
      setLoading(true);
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/v1/noticias/usuario/${usuarioActual}`);
        const data = await res.json();
        setNoticias(Array.isArray(data) ? data : []);
      } catch (err) {
        setNoticias([]);
      }
      setLoading(false);
    }
    fetchNoticias();
  }, [usuarioActual]);

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
        setMensaje("Noticia editada correctamente");
        setEditModalOpen(false);
        setEditData(null);
        // Recargar noticias
        const noticiasRes = await fetch("http://127.0.0.1:8000/api/v1/noticias");
        const noticiasData = await noticiasRes.json();
        setNoticias(Array.isArray(noticiasData) ? noticiasData.filter(n => (n.usuario || "").toLowerCase() === usuarioActual.toLowerCase()) : []);
      } else if (res.status === 404) {
        setMensaje("La noticia no existe o fue eliminada.");
      } else {
        setMensaje("Error al editar la noticia");
      }
    } catch (err) {
      setMensaje("Error de red: " + err.message);
    }
    setTimeout(() => setMensaje(""), 4000);
  };

  const handleInactivar = async (id) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/noticias/${id}/inactivar`, {
        method: "PATCH"
      });
      if (res.ok) {
        setMensaje("Noticia inactivada");
        // Recargar noticias
        const noticiasRes = await fetch("http://127.0.0.1:8000/api/v1/noticias");
        const noticiasData = await noticiasRes.json();
        setNoticias(Array.isArray(noticiasData) ? noticiasData.filter(n => n.usuario === usuarioActual) : []);
      } else {
        setMensaje("Error al inactivar la noticia");
      }
    } catch (err) {
      setMensaje("Error de red: " + err.message);
    }
    setTimeout(() => setMensaje(""), 4000);
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: '#fff6ea' }}>
      <Menu />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ width: '100%', maxWidth: 600, margin: '0 auto', padding: '32px 16px', background: '#1c2120', borderRadius: '16px', boxShadow: '0 4px 24px rgba(28,33,32,0.12)' }}>
          <h2 style={{ textAlign: 'center', color: '#f1c40f', marginBottom: 24 }}>Mis Noticias</h2>
          {mensaje && <div className="mensaje" style={{ textAlign: 'center', marginBottom: 16, color: '#f1c40f' }}>{mensaje}</div>}
          {loading ? (
            <div className="loading" style={{ textAlign: 'center', color: '#f1c40f' }}>Cargando...</div>
          ) : (
            <div className="noticias-list" style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
              {noticias.length === 0 ? (
                <div style={{ textAlign: 'center', color: '#4c5058' }}>No tienes noticias creadas.</div>
              ) : (
                noticias.map(noticia => {
                  // Usar profile_image directamente de la noticia
                  const profileImage = noticia.profile_image && noticia.profile_image.startsWith('data:image')
                    ? noticia.profile_image
                    : '/img/profile.png';
                  const username = noticia.usuario || 'Usuario';
                  return (
                    <div key={noticia.Id_Noticia} className={`noticia-card${noticia.activa ? '' : ' inactiva'}`}
                      style={{
                        background: noticia.activa ? '#121826' : '#4c5058',
                        color: noticia.activa ? '#f1c40f' : '#fff6ea',
                        borderRadius: '12px',
                        boxShadow: '0 2px 8px rgba(76,80,88,0.12)',
                        padding: '20px',
                        position: 'relative',
                        transition: 'background 0.3s',
                        border: noticia.activa ? '2px solid #f1c40f' : '2px solid #4c5058',
                      }}>
                      <div style={{ display: 'flex', alignItems: 'center', marginBottom: 12 }}>
                        <img src={profileImage} alt={`Imagen de perfil de ${username}`}
                          style={{ width: 50, height: 50, borderRadius: '50%', objectFit: 'cover', marginRight: 12, border: '2px solid #f1c40f' }} />
                        <span style={{ fontWeight: 'bold', color: '#f1c40f', fontSize: '1rem' }}>{username}</span>
                      </div>
                      <h3 style={{ margin: '0 0 8px 0', fontWeight: 'bold', fontSize: '1.2rem', color: noticia.activa ? '#f1c40f' : '#fff6ea' }}>{noticia.titulo}</h3>
                      <p style={{ margin: '0 0 8px 0', color: noticia.activa ? '#fff6ea' : '#fff6ea' }}>{noticia.resumen}</p>
                      <span className="noticia-fecha" style={{ fontSize: '0.9rem', opacity: 0.8, color: '#f1c40f' }}>{new Date(noticia.fecha_publicacion).toLocaleString()}</span>
                      <div className="noticia-actions" style={{ marginTop: 12, display: 'flex', gap: 12 }}>
                        <button className="edit-btn" style={{
                          background: '#f1c40f', color: '#1c2120', border: 'none', borderRadius: '6px', padding: '8px 16px', fontWeight: 'bold', cursor: 'pointer', boxShadow: '0 1px 4px rgba(241,196,15,0.07)'
                        }} onClick={() => handleEditClick(noticia)}>Editar</button>
                        {noticia.activa ? (
                          <button className="inactivar-btn" style={{
                            background: '#4c5058', color: '#fff6ea', border: 'none', borderRadius: '6px', padding: '8px 16px', fontWeight: 'bold', cursor: 'pointer', boxShadow: '0 1px 4px rgba(76,80,88,0.07)'
                          }} onClick={() => handleInactivar(noticia.Id_Noticia)}>Inactivar</button>
                        ) : (
                          <span className="inactiva-label" style={{ color: '#f1c40f', fontWeight: 'bold', marginLeft: 8 }}>Inactiva</span>
                        )}
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          )}
        </div>
        {editModalOpen && editData && (
          <div className="modal-overlay" style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(28,33,32,0.7)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 999 }}>
            <div className="modal" style={{ background: '#fff6ea', borderRadius: '16px', padding: '32px 24px', boxShadow: '0 4px 24px rgba(76,80,88,0.18)', minWidth: 320, maxWidth: 400 }}>
              <h3 style={{ textAlign: 'center', color: '#f1c40f', marginBottom: 16 }}>Editar Noticia</h3>
              <input name="titulo" value={editData.titulo} onChange={handleEditChange} placeholder="Título" style={{ width: '100%', marginBottom: 12, padding: '8px', borderRadius: '6px', border: '1px solid #4c5058', background: '#fff6ea', color: '#1c2120' }} />
              <textarea name="resumen" value={editData.resumen} onChange={handleEditChange} placeholder="Resumen" style={{ width: '100%', marginBottom: 12, padding: '8px', borderRadius: '6px', border: '1px solid #4c5058', background: '#fff6ea', color: '#1c2120', minHeight: 80 }} />
              <input name="enlace" value={editData.enlace} onChange={handleEditChange} placeholder="Enlace" style={{ width: '100%', marginBottom: 12, padding: '8px', borderRadius: '6px', border: '1px solid #4c5058', background: '#fff6ea', color: '#1c2120' }} />
              <div className="modal-actions" style={{ display: 'flex', justifyContent: 'center', gap: 16 }}>
                <button onClick={handleEditSave} style={{ background: '#f1c40f', color: '#1c2120', border: 'none', borderRadius: '6px', padding: '8px 24px', fontWeight: 'bold', cursor: 'pointer' }}>Guardar</button>
                <button onClick={() => setEditModalOpen(false)} style={{ background: '#4c5058', color: '#fff6ea', border: 'none', borderRadius: '6px', padding: '8px 24px', fontWeight: 'bold', cursor: 'pointer' }}>Cancelar</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
