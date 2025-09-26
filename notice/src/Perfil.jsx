import React from "react";
import { useNavigate } from "react-router-dom";
import "./perfil.css";

const Perfil = () => {
  const navigate = useNavigate();

  const user = {
    fullName: "Juan David Rojas Burbano",
    email: "juan.david.rojas0@gmail.com",
    phone: "3202960539",
    address: "Cra 31 # 29-58 Cundinamarca, Bogota",
    country: "Colombia",
  };

  const handleEdit = () => {
    navigate("/edit", { state: { user } });
  };

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
              <img src="/img/profile.png" alt="User" />
            </div>
          </div>
          <h2>Rulitos08</h2>

          {/* Redes */}
          <div className="social-info">
            <div className="social-row">
              <img src="/img/twitter.png" alt="Twitter" />
              <span>Twitter</span>
              <span className="twitter-handle">@Rulitos088</span>
            </div>
            <hr className="linea-negra" />
            <div className="social-row">
              <img src="/img/telephone.png" alt="Phone" />
              <span>Cellphone</span>
              <span className="twitter-handle">+57 3202960539</span>
            </div>
            <hr className="linea-negra" />
          </div>
        </div>

        {/* Información detallada */}
        <div className="profile-details">
          <div className="info-row">
            <span className="label">Full Name</span>
            <span className="value">{user.fullName}</span>
          </div>
          <div className="info-row">
            <span className="label">Email</span>
            <span className="value">{user.email}</span>
          </div>
          <div className="info-row">
            <span className="label">Phone</span>
            <span className="value">{user.phone}</span>
          </div>
          <div className="info-row">
            <span className="label">Address</span>
            <span className="value">{user.address}</span>
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
