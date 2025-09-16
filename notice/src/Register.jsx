import React, { useState } from "react";
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
      <h2>Regístrate</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="usua_nombre">Nombres</label>
          <input
            type="text"
            id="usua_nombre"
            name="usua_nombre"
            value={formData.usua_nombre}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="usua_apellido">Apellidos</label>
          <input
            type="text"
            id="usua_apellido"
            name="usua_apellido"
            value={formData.usua_apellido}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="usua_celular">Celular</label>
          <input
            type="text"
            id="usua_celular"
            name="usua_celular"
            value={formData.usua_celular}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="usua_direccion">Dirección</label>
          <input
            type="text"
            id="usua_direccion"
            name="usua_direccion"
            value={formData.usua_direccion}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="usua_email">Email</label>
          <input
            type="email"
            id="usua_email"
            name="usua_email"
            value={formData.usua_email}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="usua_pais">País</label>
          <input
            type="text"
            id="usua_pais"
            name="usua_pais"
            value={formData.usua_pais}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="usua_usuario">Usuario</label>
          <input
            type="text"
            id="usua_usuario"
            name="usua_usuario"
            value={formData.usua_usuario}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="usua_password">Contraseña</label>
          <input
            type="password"
            id="usua_password"
            name="usua_password"
            value={formData.usua_password}
            onChange={handleChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="usua_rol_fk">Rol</label>
          <select
            id="usua_rol_fk"
            name="usua_rol_fk"
            value={formData.usua_rol_fk}
            onChange={handleChange}
          >
            <option disabled>administrador</option>
            <option value="usuario">usuario</option>
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
  );
};

export default Register;
