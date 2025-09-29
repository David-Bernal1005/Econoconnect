import React from "react";
import "./bienvenida.css";

const Bienvenida = ({ name, onLogout }) => {
  if (!name) return null;
  return (
    <div className="bienvenida-box">
      <span>Bienvenido, {name}</span>
      <button className="logout-btn" onClick={onLogout}>Cerrar sesión</button>
    </div>
  );
};

export default Bienvenida;
