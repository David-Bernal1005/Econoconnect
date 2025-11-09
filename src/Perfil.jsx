import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./perfil.css";

const Perfil = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [suggestedUsers, setSuggestedUsers] = useState([]);
  const [followersCount, setFollowersCount] = useState(0); // 👈 nuevo estado

  // 🧠 1️⃣ Obtener usuario actual
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("No autenticado");
      setLoading(false);
      return;
    }

    fetch("http://localhost:8000/api/v1/users/me", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error("No se pudo obtener el usuario");
        return res.json();
      })
      .then((data) => {
        setUser(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error usuario:", err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // 🧠 2️⃣ Obtener cantidad de seguidores del usuario
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token || !user) return;

    fetch(`http://localhost:8000/api/v1/seguidores/count/${user.id_user}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Error al obtener seguidores");
        return res.json();
      })
      .then((data) => {
        setFollowersCount(data.seguidores || 0);
      })
      .catch((err) => {
        console.error("Error en seguidores:", err);
        setFollowersCount(0);
      });
  }, [user]); // 👈 se ejecuta cuando ya se tiene el user

  // 🧠 3️⃣ Obtener sugerencias para seguir
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    fetch("http://localhost:8000/api/v1/seguidores/sugerencias", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Error al obtener sugerencias");
        return res.json();
      })
      .then((data) => setSuggestedUsers(Array.isArray(data) ? data : []))
      .catch((err) => {
        console.error("Error en sugerencias:", err);
        setSuggestedUsers([]);
      });
  }, []);

  // 🧠 4️⃣ Acción al seguir usuario
  const handleFollow = async (userId) => {
    const token = localStorage.getItem("token");
    try {
      const res = await fetch("http://localhost:8000/api/v1/seguidores/seguir", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ id_user_seguido: userId }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Error al seguir usuario");
      }

      alert("Ahora sigues a este usuario ✅");

      // 🔁 Actualizar contador de seguidores si el usuario actual es seguido
      if (userId === user.id_user) {
        setFollowersCount((prev) => prev + 1);
      }

    } catch (err) {
      alert(err.message);
    }
  };

  const handleUnfollow = async (userId) => {
    const token = localStorage.getItem("token");
    try {
      const res = await fetch("http://localhost:8000/api/v1/seguidores/unfollow", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ id_user_seguido: userId }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Error al dejar de seguir usuario");
      }

      alert("Has dejado de seguir al usuario ❌");

      if (userId === user.id_user) {
        setFollowersCount((prev) => Math.max(prev - 1, 0));
      }

    } catch (err) {
      alert(err.message);
    }
  };

  const handleEdit = () => navigate("/edit-user", { state: { user } });

  if (loading) return <p style={{ color: "#fff" }}>Cargando...</p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!user) return <p>No se encontraron datos de usuario.</p>;

  return (
    <div>
      {/* Sidebar */}
      <div className="slidebar">
        <ul>
          <a href="/perfil">
            <img src="/img/perfil.svg" alt="Perfil" />
            <span>perfil</span>
          </a>
        </ul>

        <ul>
          <a href="/">
            <img src="/img/inicio.svg" alt="Inicio" />
            <span>Inicio</span>
          </a>
        </ul>
        <ul>
          <a href="/chat">
            <img src="/img/chats.svg" alt="Chats" />
            <span>Chats</span>
          </a>
        </ul>
        <ul>
          <a href="/graficas">
            <img src="/img/graficos.svg" alt="Graficas" />
            <span>Graficas</span>
          </a>
        </ul>
        <ul>
          <a href="/creaciones">
            <img src="/img/creaciones.svg" alt="Creaciones" />
            <span>Creaciones</span>
          </a>
        </ul>
      </div>

      {/* Contenido perfil */}
      <div className="i1">
        <div className="profile-card1">
          <div className="profile-header">
            <img src="/img/monedas.png" alt="Monedas" className="header-img" />
            <div className="profile-pic">
              {user.profile_image ? (
                <img src={user.profile_image} alt="User" />
              ) : (
                <img src="/img/profile.png" alt="User" />
              )}
            </div>
          </div>
          <h2>{user.username}</h2>

          {/* Redes */}
          <div className="social-info">
            <div className="social-row">
              <img src="/img/twitter.png" alt="Twitter" />
              <span>Twitter</span>
              <span className="twitter-handle">@{user.username}</span>
            </div>
            <hr className="linea-negra" />
            <div className="social-row">
              <img src="/img/telephone.png" alt="Phone" />
              <span>Cellphone</span>
              <span className="twitter-handle">{user.cellphone}</span>
            </div>
            <hr className="linea-negra" />
            <div className="social-row">
              <span>Seguidores:</span>
              <span className="twitter-handle">{followersCount}</span> {/* 👈 contador dinámico */}
            </div>
          </div>
        </div>

        {/* Columna derecha */}
        <div className="right-column">
          {/* Información detallada */}
          <div className="profile-details">
            <div className="info-row">
              <span className="label">Full Name</span>
              <span className="value">
                {user.name} {user.lastname}
              </span>
            </div>
            <div className="info-row">
              <span className="label">Email</span>
              <span className="value">{user.email}</span>
            </div>
            <div className="info-row">
              <span className="label">Phone</span>
              <span className="value">{user.cellphone}</span>
            </div>
            <div className="info-row">
              <span className="label">Address</span>
              <span className="value">{user.direction}</span>
            </div>
            <div className="info-row">
              <span className="label">Country</span>
              <span className="value">
                {user.pais ? user.pais.nombre : user.country || "No especificado"}
              </span>
            </div>
            <div className="info-button">
              <button onClick={handleEdit}>Edit</button>
            </div>
          </div>

          {/* Seguidores */}
          <div className="seguidores">
            <h3>Sugerencias para seguir</h3>
            <div className="user-list">
              {suggestedUsers.length > 0 ? (
                suggestedUsers.map((u) => (
                  <div className="user-card" key={u.id_user}>
                    <img
                      src={u.profile_image || "/img/profile.png"}
                      alt={u.username}
                      className="user-avatar"
                    />
                    <div className="user-info">
                      <h4>@{u.username}</h4>
                      <p>
                        {u.name} {u.lastname}
                      </p>
                      {u.is_following ? (
                        <button
                          className="follow-btn unfollow"
                          onClick={() => handleUnfollow(u.id_user)}
                        >
                          Dejar de seguir
                        </button>
                      ) : (
                        <button
                          className="follow-btn"
                          onClick={() => handleFollow(u.id_user)}
                        >
                          Seguir
                        </button>
                      )}
                    </div>
                  </div>
                ))
              ) : (
                <p>No hay usuarios para seguir</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Perfil;
