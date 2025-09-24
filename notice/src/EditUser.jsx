import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./EditUser.css"; // 👈 Aquí importas el CSS separado

const EditUser = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = location.state || {};

  const [formData, setFormData] = useState(
    user || { fullName: "", email: "", phone: "", address: "", country: "" }
  );

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSave = () => {
    console.log("Usuario actualizado:", formData);
    navigate("/perfil");
  };

  return (
    <div className="edit-user">
      <h2>Editar usuario</h2>
      <form>
        <div className="info-row">
          <label className="label">Full Name</label>
          <input
            className="value"
            type="text"
            name="fullName"
            value={formData.fullName}
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
          <label className="label">Phone</label>
          <input
            className="value"
            type="text"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
          />
        </div>

        <div className="info-row">
          <label className="label">Address</label>
          <input
            className="value"
            type="text"
            name="address"
            value={formData.address}
            onChange={handleChange}
          />
        </div>

        <div className="info-row">
          <label className="label">Country</label>
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
            Save
          </button>
        </div>
      </form>
    </div>
  );
};

export default EditUser;
