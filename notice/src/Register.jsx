import React, { useState } from "react";
import { FaUser, FaUserTag, FaPhone, FaHome, FaEnvelope, FaGlobe, FaUserCircle, FaLock, FaUserShield, FaDoorClosed } from "react-icons/fa";
import "./register.css";

const Register = () => {
  const [formData, setFormData] = useState({
    name: "",
    lastname: "",
    cellphone: "",
    direction: "",
    email: "",
    country: "",
    username: "",
    password: "",
    rol: "usuario",
    state: "activo"
  });

  const [mensaje, setMensaje] = useState("");

  const handleChange = (e) => {
  setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch("http://localhost:8000/api/v1/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(formData)
    })
      .then(async (res) => {
        if (res.ok) {
          setMensaje("✅ Registro exitoso");
        } else {
          const error = await res.text();
          setMensaje("❌ Error: " + error);
        }
      })
      .catch((err) => {
        setMensaje("❌ Error de conexión");
      });
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
            id="name"
            name="name"
            value={formData.name}
            placeholder=" Nombre..."            
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaUserTag />
          <input
            type="text"
            id="lastname"
            name="lastname"
            value={formData.lastname}
            placeholder=" Apellido..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaPhone />
          <input
            type="text"
            id="cellphone"
            name="cellphone"
            value={formData.cellphone}
            placeholder=" Celular..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaHome />
          <input
            type="text"
            id="direction"
            name="direction"
            value={formData.direction}
            placeholder=" Dirección..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaEnvelope />
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            placeholder=" Email..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaGlobe />
          <input
            type="text"
            id="country"
            name="country"
            value={formData.country}
            placeholder=" País..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaUserCircle />
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            placeholder=" Usuario..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaLock />
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            placeholder=" Contraseña..."
            onChange={handleChange}
          />
        </div>

        <div className="input-group">
          <FaUserShield />
          <select
            id="rol"
            name="rol"
            value={formData.rol}
            onChange={handleChange}
          >
            <option value="administrador">Administrador</option>
            <option value="usuario">Usuario</option>
          </select>
        </div>

        <button type="submit">Registrarse</button>
      </form>

      {mensaje && (
        <div
          id="mensaje"
          style={{
            marginTop: "10px",
            color: mensaje.includes("exitoso") ? "#388e3c" : "#d32f2f",
            fontWeight: "bold"
          }}
        >
          {mensaje}
        </div>
      )}
      <a href="/login" className="back-link">Login</a>
      </div>



    </div>
  );
};

export default Register;
