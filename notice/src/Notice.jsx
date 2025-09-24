import React from 'react';
import './notice.css';




const Notice = ({ noticia }) => {
  if (!noticia) return (
    <div className="news-container" style={{ justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
      <span style={{ color: '#fff' }}>No hay datos de la noticia.</span>
    </div>
  );

  // Normaliza los datos para mostrar correctamente
  const username = noticia.usuario || noticia.Usuario || 'Usuario';
  const avatarSrc = '/img/profile.svg';
  const title = noticia.Titulo || noticia.titulo || noticia.title || 'Sin título';
  const text = noticia.Contenido || noticia.resumen || noticia.text || 'Sin contenido';
  const link = noticia.Fuente || noticia.enlace || noticia.link || '';
  const linkText = link ? link.replace(/^https?:\/\//, '').replace(/\/$/, '') : '';

  return (
    <div className="news-container">
      <div className="sidebar">
        <button className="sidebar-button">Divisas</button>
        <button className="sidebar-button">M. Internacional</button>
        <button className="sidebar-button">Criptomonedas</button>
      </div>

      <div className="content">
        <div className="user-info">
          <div className="avatar">
            <img src={avatarSrc} alt="avatar" />
          </div>
          <span className="username">{username}</span>
        </div>

        <div className="news-box">
          <h3 className="news-title">{title}</h3>
          <p className="news-text">{text}</p>
          {link && (
            <a href={link} className="news-link" target="_blank" rel="noopener noreferrer">{linkText}</a>
          )}
        </div>
      </div>
    </div>
  );
};

export default Notice;
