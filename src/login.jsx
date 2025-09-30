import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./login.css";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) throw new Error("Usuario o contraseña incorrectos");

      const data = await res.json();

  localStorage.setItem("token", data.access_token);
  localStorage.setItem("nombre_usuario", data.name);
  localStorage.setItem("user_id", data.id_user);
  setMessage("Inicio de sesión exitoso");
  window.location.href = "/";

    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <div className="login-page">
      <div className="login-wrapper">

        {/* LADO IZQUIERDO (imagen de fondo + texto, SIN icono) */}
        <div className="login-branding">
          <div className="branding-overlay">
            <h1>Econoconnect</h1>
            <p>
              Red Social de Economía, donde la educación financiera es para todos: aprende, comparte y crece con nosotros.
            </p>
          </div>
        </div>

        {/* LADO DERECHO (formulario tipo imagen anterior) */}
        <div className="login-container">
          <div className="login-logo">
            <img src="/img/logo-ec.png" alt="Econoconnect" />
          </div>
          <h2>Inicia Sesión</h2>

          <form onSubmit={handleSubmit} className="login-form">
            <label>Usuario:</label>
            <div className="input-group">
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            <label>Contraseña:</label>
            <div className="input-group">
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <div className="login-options">
              <Link to="/forgot" className="forgot-link">
                Forgot Password?
              </Link>
              <label className="remember-me">
                <input type="checkbox" />
                Remember Me
              </label>
            </div>

            <button type="submit" className="login-button">
              LOGIN
            </button>
          </form>

          {message && (
            <p
              className="login-message"
              style={{
                color: message.includes("exitoso") ? "#27ae60" : "#e74c3c",
              }}
            >
              {message}
            </p>
          )}

          <p className="signup-text">
            Don’t have an account?{" "}
            <Link to="/register" className="signup-link">
              Register
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
