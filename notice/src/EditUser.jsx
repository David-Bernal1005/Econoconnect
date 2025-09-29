
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./EditUser.css";

const EditUser = () => {

  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    lastname: "",
    email: "",
    cellphone: "",
    direction: "",
    country: ""
  });
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
        setFormData({
          name: data.name || "",
          lastname: data.lastname || "",
          email: data.email || "",
          cellphone: data.cellphone || "",
          direction: data.direction || "",
          country: data.country || ""
        });
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);


  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };


  const handleSave = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("No autenticado");
      return;
    }
    try {
      const res = await fetch("http://localhost:8000/api/v1/users/me", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });
      if (!res.ok) throw new Error("No se pudo actualizar el usuario");
      const data = await res.json();
      alert("Usuario actualizado correctamente");
      navigate("/perfil");
    } catch (err) {
      alert("Error al actualizar: " + err.message);
    }
  };


  if (loading) return <p>Cargando...</p>;
  if (error) return <p style={{color: 'red'}}>{error}</p>;

  return (
    <div className="edit-user">
      <h2>Editar usuario</h2>
      <form>
        <div className="info-row">
          <label className="label">Nombre</label>
          <input
            className="value"
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
          />
        </div>
        <div className="info-row">
          <label className="label">Apellido</label>
          <input
            className="value"
            type="text"
            name="lastname"
            value={formData.lastname}
            onChange={handleChange}
          />
        </div>
        <div className="info-row">
          <label className="label">Email</label>
          <input
            className="value"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
        </div>
        <div className="info-row">
          <label className="label">Teléfono</label>
          <input
            className="value"
            type="text"
            name="cellphone"
            value={formData.cellphone}
            onChange={handleChange}
          />
        </div>
        <div className="info-row">
          <label className="label">Dirección</label>
          <input
            className="value"
            type="text"
            name="direction"
            value={formData.direction}
            onChange={handleChange}
          />
        </div>
        <div className="info-row">
          <label className="label">País</label>
          <input
            className="value"
            type="text"
            name="country"
            value={formData.country}
            onChange={handleChange}
          />
        </div>
        <div className="info-button">
          <button type="button" onClick={handleSave}>
            Guardar
          </button>
        </div>
      </form>
    </div>
  );
};

export default EditUser;
