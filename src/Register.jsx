import React, { useState } from "react";
import { FaUser, FaUserTag, FaEnvelope, FaUserCircle, FaLock } from "react-icons/fa";
import "./register.css";

const Register = () => {
  const [formData, setFormData] = useState({
    usua_nombre: "",
    usua_apellido: "",
    usua_email: "",
    usua_usuario: "",
    usua_password: "",
    usua_rol_fk: "usuario",
  });
  const [mensaje, setMensaje] = useState("");
  const [mensajeColor, setMensajeColor] = useState("#d32f2f");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");
    setMensajeColor("#d32f2f");
    try {
      const response = await fetch("http://localhost:8000/api/v1/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: formData.usua_nombre,
          lastname: formData.usua_apellido,
          email: formData.usua_email,
          username: formData.usua_usuario,
          password: formData.usua_password,
          rol: "usuario",
        }),
      });
      if (response.ok) {
        setMensaje("✅ Registro exitoso");
        setMensajeColor("#388e3c");
      } else {
        const data = await response.json();
        const detail = data.detail;
        setMensaje(typeof detail === 'string' ? detail : JSON.stringify(detail) || "Error en el registro");
        setMensajeColor("#d32f2f");
      }
    } catch (err) {
      setMensaje("Error de conexión");
      setMensajeColor("#d32f2f");
    }
  };

  return (
    <div className="register-page">
      <div className="register-wrapper">
        <div className="register-container">
          <div className="register-logo">
            <img src="/img/logo-ec.png" alt="Econoconnect" />
          </div>
          <h1 className="register-title">Registrate</h1>
          <p className="register-subtitle">Únete a nuestra comunidad y conecta con nuevas oportunidades.</p>

          <form className="register-form" onSubmit={handleSubmit}>
  <div className="form-group">
    <label htmlFor="usua_nombre">Nombre</label>
    <div className="input-group">
      <FaUser />
      <input
        id="usua_nombre"
        type="text"
        name="usua_nombre"
        value={formData.usua_nombre}
        placeholder="Nombre..."
        onChange={handleChange}
      />
    </div>
  </div>

  <div className="form-group">
    <label htmlFor="usua_apellido">Apellido</label>
    <div className="input-group">
      <FaUserTag />
      <input
        id="usua_apellido"
        type="text"
        name="usua_apellido"
        value={formData.usua_apellido}
        placeholder="Apellido..."
        onChange={handleChange}
      />
    </div>
  </div>

  <div className="form-group">
    <label htmlFor="usua_email">Email</label>
    <div className="input-group">
      <FaEnvelope />
      <input
        id="usua_email"
        type="email"
        name="usua_email"
        value={formData.usua_email}
        placeholder="Email..."
        onChange={handleChange}
      />
    </div>
  </div>

  <div className="form-group">
    <label htmlFor="usua_usuario">Usuario</label>
    <div className="input-group">
      <FaUserCircle />
      <input
        id="usua_usuario"
        type="text"
        name="usua_usuario"
        value={formData.usua_usuario}
        placeholder="Usuario..."
        onChange={handleChange}
      />
    </div>
  </div>

  <div className="form-group">
    <label htmlFor="usua_password">Contraseña</label>
    <div className="input-group">
      <FaLock />
      <input
        id="usua_password"
        type="password"
        name="usua_password"
        value={formData.usua_password}
        placeholder="Contraseña..."
        onChange={handleChange}
      />
    </div>
  </div>

  <button type="submit" className="register-button">Registrarse</button>
</form>


          {mensaje && (
            <p className="register-message" style={{ color: mensajeColor }}>{mensaje}</p>
          )}

          <p className="login-text">
            ¿Ya tienes cuenta? <a href="/login" className="login-link">Inicia sesión</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
