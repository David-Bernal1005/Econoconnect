// src/pages/Login.jsx
import React, { useState } from "react";
import { Link } from "react-router-dom";
import { FaBolt, FaDoorClosed, FaEnvelope, FaLock } from "react-icons/fa";
import "./login.css"; // ajusta la ruta si tu login.css está en otra carpeta

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        throw new Error("Usuario o contraseña incorrectos");
      }

      const data = await res.json();
      localStorage.setItem("token", data.access_token);

      setMessage("Inicio de sesión exitoso");
      // Si usas React Router → redirige con navigate
      window.location.href = "/dashboard";
    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <div className="container">
      <div className="header-icon">
        <FaBolt />
        <a href="/login">
          <FaDoorClosed />
        </a>
      </div>

      <div className="header">Login</div>

      <form onSubmit={handleSubmit}>
        <div className="login-box">
          <div className="login-title">Bienvenido</div>

          <div className="input-group">
            <FaEnvelope />
            <input
              type="text"
              value={username}
              placeholder="username..."
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className="input-group">
            <FaLock />
            <input
              type="password"
              value={password}
              placeholder="Contraseña..."
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <a href="/forgot">
            <div className="forgot">¿Olvidaste tu contraseña?</div>
          </a>
          <Link to="/register" className="forgot">
                Registrarse
          </Link>


          <button className="btn" type="submit">
            Listo <span>🙂</span>
          </button>
        </div>
      </form>

      <p id="message">{message}</p>
    </div>
  );
};

export default Login;
