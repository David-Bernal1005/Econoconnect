import React, { useEffect, useState } from 'react';
import './notice.css';




const Notice = ({ noticia }) => {
  // Depuración: mostrar noticia y usuario en consola
  console.log('noticia:', noticia);
  if (noticia && noticia.usuario) {
    console.log('noticia.usuario:', noticia.usuario);
  }
  if (!noticia) return (
    <div className="news-container" style={{ justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
      <span style={{ color: '#fff' }}>No hay datos de la noticia.</span>
    </div>
  );

  // Normaliza los datos para mostrar correctamente
  // Mostrar nombre y foto del usuario creador de la noticia (igual que en Perfil.jsx)
  let username = 'Usuario';
  let userImage = '/img/profile.png';
  if (noticia && noticia.usuario) {
    if (typeof noticia.usuario === 'object') {
      username = noticia.usuario.username || noticia.usuario.name || noticia.usuario.Usuario || 'Usuario';
      if (noticia.usuario.profile_image && noticia.usuario.profile_image.startsWith('data:image')) {
        userImage = noticia.usuario.profile_image;
      }
    } else {
      username = noticia.usuario;
    }
  }
  // Si la noticia tiene profile_image directo, úsalo
  if (noticia && noticia.profile_image && noticia.profile_image.startsWith('data:image')) {
    userImage = noticia.profile_image;
  }
  // Si el usuario logueado es el mismo que el de la noticia, usa su imagen de perfil de localStorage
  try {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.username === username && user.profile_image && user.profile_image.startsWith('data:image')) {
      userImage = user.profile_image;
    }
  } catch {}
  const avatarSrc = '/img/profile.svg';
  const title = noticia.Titulo || noticia.titulo || noticia.title || 'Sin título';
  const text = noticia.Contenido || noticia.resumen || noticia.text || 'Sin contenido';
  const link = noticia.Fuente || noticia.enlace || noticia.link || '';
  const linkText = link ? link.replace(/^https?:\/\//, '').replace(/\/$/, '') : '';

    // Eliminado useEffect y estado, solo lógica directa arriba

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
            {userImage && userImage.startsWith('data:image') ? (
              <img src={userImage} alt="User" />
            ) : (
              <img src="/img/profile.png" alt="User" />
            )}
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
