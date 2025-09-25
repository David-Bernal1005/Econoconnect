// src/pages/Login.jsx
import React, { useState } from "react";
import { Link } from "react-router-dom";
import { FaBolt, FaDoorClosed, FaUserCircle, FaLock } from "react-icons/fa";
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
  localStorage.setItem("nombre_usuario", data.name);
  setMessage("Inicio de sesión exitoso");
  window.location.href = "/";
    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <div className="container">
            <div className="sign-out">
        <a href="/">
          <img src="img/exit.svg" alt="Exit" />
        </a>
      </div>
      <div className="header-icon">
        <a href="/">
          <FaDoorClosed />
        </a>
      </div>

      <div className="header">Login</div>

      <form onSubmit={handleSubmit}>
        <div className="login-box">
          <div className="login-title">Bienvenido</div>

          <div className="input-group">
            <FaUserCircle />
            <input
              type="text"
              value={username}
              placeholder=" Usuario..."
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

          <button className="btn" type="submit">
            Listo <span>🙂</span>
          </button>

          <a href="/forgot">
            <div className="back-link">¿Olvidaste tu contraseña?</div>
          </a>
          <Link to="/register" className="back-link">
            Registrarse
          </Link>

        {message && (
          <p
            id="message"
            style={{
              marginTop: "10px",
              color: message.includes("exitoso") ? "#388e3c" : "#d32f2f",
              fontWeight: "bold"
            }}
          >
            {message}
          </p>
        )}
        </div>
        </form>
      </div>
  );
};

export default Login;