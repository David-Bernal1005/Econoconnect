
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
    country: "",
    id_pais: null,
    profile_image: ""
  });
  const [paises, setPaises] = useState([]);
  const [preview, setPreview] = useState("");
  // Mostrar preview si ya hay imagen
  useEffect(() => {
    if (formData.profile_image) {
      setPreview(formData.profile_image);
    }
  }, [formData.profile_image]);
  // Manejar selección de archivo y convertir a base64
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onloadend = () => {
      setFormData((prev) => ({ ...prev, profile_image: reader.result }));
      setPreview(reader.result);
    };
    reader.readAsDataURL(file);
  };
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("No autenticado");
      setLoading(false);
      return;
    }

    // Cargar datos del usuario y países en paralelo
    Promise.all([
      fetch("http://localhost:8000/api/v1/users/me", {
        headers: { "Authorization": `Bearer ${token}` }
      }),
      fetch("http://localhost:8000/api/v1/paises")
    ])
      .then(async ([userRes, paisesRes]) => {
        if (!userRes.ok) throw new Error("No se pudo obtener el usuario");
        if (!paisesRes.ok) throw new Error("No se pudieron cargar los países");
        
        const userData = await userRes.json();
        const paisesData = await paisesRes.json();
        
        setFormData({
          name: userData.name || "",
          lastname: userData.lastname || "",
          email: userData.email || "",
          cellphone: userData.cellphone || "",
          direction: userData.direction || "",
          country: userData.country || "",
          id_pais: userData.id_pais || null,
          profile_image: userData.profile_image || ""
        });
        setPaises(paisesData);
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
          <label className="label">Foto de perfil</label>
          <input type="file" accept="image/*" onChange={handleImageChange} />
        </div>
        {preview && (
          <div className="info-row">
            <img src={preview} alt="Preview" style={{ width: 100, height: 100, borderRadius: "50%" }} />
          </div>
        )}
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
          <select
            className="value"
            name="id_pais"
            value={formData.id_pais || ""}
            onChange={handleChange}
          >
            <option value="">Seleccionar país...</option>
            {paises.map((pais) => (
              <option key={pais.id_pais} value={pais.id_pais}>
                {pais.nombre} {pais.codigo_telefono && `(${pais.codigo_telefono})`}
              </option>
            ))}
          </select>
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
