import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./perfil.css";

const Perfil = () => {

  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("No autenticado");
      setLoading(false);
      return;
    }
    fetch("http://localhost:8000/api/v1/users/me", {
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("No se pudo obtener el usuario");
        return res.json();
      })
      .then((data) => {
        setUser(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [navigate]);


  const handleEdit = () => {
    navigate("/edit-user", { state: { user } });
  };

  if (loading) return <p>Cargando...</p>;
  if (error) return <p style={{color: 'red'}}>{error}</p>;
  if (!user) return <p>No se encontraron datos de usuario.</p>;

  return (
    <div>
      {/* Sidebar */}
      <div className="slidebar">
        <ul>
          <a href="/perfil">
            <img src="/img/perfil.svg" alt="Perfil" />
            <span>perfil</span>
          </a>
        </ul>
        <ul>
          <a href="/">
            <img src="/img/inicio.svg" alt="Inicio" />
            <span>Inicio</span>
          </a>
        </ul>
        <ul>
          <a href="/chats">
            <img src="/img/chats.svg" alt="Chats" />
            <span>Chats</span>
          </a>
        </ul>
        <ul>
          <a href="/graficas">
            <img src="/img/graficos.svg" alt="Graficas" />
            <span>Graficas</span>
          </a>
        </ul>
        <ul>
          <a href="/creaciones">
            <img src="/img/creaciones.svg" alt="Creaciones" />
            <span>Creaciones</span>
          </a>
        </ul>
      </div>

      {/* Botón salir */}
      <div className="sign-out">
        <a href="/exit">
          <img src="/img/exit.svg" alt="Exit" />
        </a>
      </div>

      {/* Contenido perfil */}
      <div className="i1">
        <div className="profile-card1">
          <div className="profile-header">
            <img src="/img/monedas.png" alt="Monedas" className="header-img" />
            <div className="profile-pic">
              {user.profile_image ? (
                <img src={user.profile_image} alt="User" />
              ) : (
                <img src="/img/profile.png" alt="User" />
              )}
            </div>
          </div>
          <h2>{user.username}</h2>

          {/* Redes */}
          <div className="social-info">
            <div className="social-row">
              <img src="/img/twitter.png" alt="Twitter" />
              <span>Twitter</span>
              <span className="twitter-handle">@{user.username}</span>
            </div>
            <hr className="linea-negra" />
            <div className="social-row">
              <img src="/img/telephone.png" alt="Phone" />
              <span>Cellphone</span>
              <span className="twitter-handle">{user.cellphone}</span>
            </div>
            <hr className="linea-negra" />
          </div>
        </div>

        {/* Información detallada */}
        <div className="profile-details">
          <div className="info-row">
            <span className="label">Full Name</span>
            <span className="value">{user.name} {user.lastname}</span>
          </div>
          <div className="info-row">
            <span className="label">Email</span>
            <span className="value">{user.email}</span>
          </div>
          <div className="info-row">
            <span className="label">Phone</span>
            <span className="value">{user.cellphone}</span>
          </div>
          <div className="info-row">
            <span className="label">Address</span>
            <span className="value">{user.direction}</span>
          </div>
          <div className="info-row">
            <span className="label">Country</span>
            <span className="value">{user.country}</span>
          </div>
          <div className="info-button">
            <button onClick={handleEdit}>Edit</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Perfil;
