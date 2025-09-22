import React, { useState } from "react";
import { FaUser, FaUserTag, FaPhone, FaHome, FaEnvelope, FaGlobe, FaUserCircle, FaLock, FaUserShield, FaDoorClosed } from "react-icons/fa";
import "./register.css";

const Register = () => {
  const [formData, setFormData] = useState({
    usua_nombre: "",
    usua_apellido: "",
    usua_celular: "",
    usua_direccion: "",
    usua_email: "",
    usua_pais: "",
    usua_usuario: "",
    usua_password: "",
    usua_rol_fk: "usuario",
  });

  const [mensaje, setMensaje] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Aquí iría la lógica de tu servicio register.js
    console.log("Datos enviados:", formData);

    setMensaje("✅ Registro exitoso"); // puedes cambiarlo según respuesta del backend
  };

  return (
    <div className="register-container">
      <div className="header-icon">
        <a href="/">
          <FaDoorClosed />
        </a>
      </div>
      <div className="header">Regístrate</div>
      <div className="register-box">
        <div className="register-title">Bienvenido</div>
        <form onSubmit={handleSubmit}>

        <div className="input-group">
          <FaUser />
          <input
            type="text"
            id="usua_nombre"
            name="usua_nombre"
            value={formData.usua_nombre}
            placeholder=" Nombre..."            
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaUserTag />
          <input
            type="text"
            id="usua_apellido"
            name="usua_apellido"
            value={formData.usua_apellido}
            placeholder=" Apellido..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaPhone />
          <input
            type="text"
            id="usua_celular"
            name="usua_celular"
            value={formData.usua_celular}
            placeholder=" Celular..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaHome />
          <input
            type="text"
            id="usua_direccion"
            name="usua_direccion"
            value={formData.usua_direccion}
            placeholder=" Dirección..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaEnvelope />
          <input
            type="email"
            id="usua_email"
            name="usua_email"
            value={formData.usua_email}
            placeholder=" Email..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaGlobe />
          <input
            type="text"
            id="usua_pais"
            name="usua_pais"
            value={formData.usua_pais}
            placeholder=" País..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaUserCircle />
          <input
            type="text"
            id="usua_usuario"
            name="usua_usuario"
            value={formData.usua_usuario}
            placeholder=" Usuario..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaLock />
          <input
            type="password"
            id="usua_password"
            name="usua_password"
            value={formData.usua_password}
            placeholder=" Contraseña..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaUserShield />
          <select
            id="usua_rol_fk"
            name="usua_rol_fk"
            value={formData.usua_rol_fk}
            onChange={handleChange}
          >
            <option disabled>Administrador</option>
            <option value="usuario">Usuario</option>
          </select>
        </div>

        <button type="submit">Registrarse</button>
      </form>

      {mensaje && (
        <div id="mensaje" style={{ marginTop: "10px", color: "#d32f2f" }}>
      {mensaje}
      </div>
      )}
      <a href="/login" className="back-link">Login</a>
      </div>



    </div>
  );
};

export default Register;
