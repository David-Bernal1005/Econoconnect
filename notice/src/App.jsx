import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Menu from "./Menu";
import Bienvenida from "./Bienvenida";
import Login from "./login"; 
import Search from "./Search";
import Exit from "./Exit";
import Carousel from "./Carousel";
import Notice from "./Notice";
import Filter from "./Filter";
import Register from "./Register";
import ForgotPassword from "./ForgotPassword";
import MisNoticias from "./MisNoticias";
import Creaciones from "./Creaciones";

import Perfil from "./Perfil";
import EditUser from "./EditUser";

import Graficas from "./Graficas"; 

import Chat from "./Chat";



import "./app.css";

const App = () => {
  const [match, setMatch] = useState(false);
  const [searching, setSearching] = useState(false);
  const [noticias, setNoticias] = useState([]);
  const [nombreUsuario, setNombreUsuario] = useState(
    localStorage.getItem("nombre_usuario")
  );

  useEffect(() => {
    setNombreUsuario(localStorage.getItem("nombre_usuario"));
    fetch("http://localhost:8000/api/v1/noticias")
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setNoticias(data);
        } else {
          setNoticias([]);
        }
      })
      .catch(() => setNoticias([]));
  }, []);

  const handleSearch = (result) => {
    setMatch(result.match);
    setSearching(result.searching);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("nombre_usuario");
    setNombreUsuario("");
    window.location.href = "/";
  };

  const isLogged = Boolean(localStorage.getItem("token"));

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <div className="main-layout">
              <aside>
                {isLogged && <Menu />}
                {isLogged && <Exit />}
                {isLogged && <Filter />}
                {!isLogged && (
                  <a
                    href="/login"
                    className="back-link"
                    style={{
                      position: "fixed",
                      top: 30,
                      right: 30,
                      zIndex: 9999,
                      background: "#ffcc00",
                      color: "#1c2120",
                      padding: "10px 20px",
                      borderRadius: "8px",
                      fontWeight: "bold",
                      textDecoration: "none",
                    }}
                  >
                    Login
                  </a>
                )}
              </aside>
              <div className="main-content">
                <Search noticias={noticias} onSearch={handleSearch} />
                <section className="content-section">
                  {!searching && <Carousel />}
                </section>
              </div>
              <Bienvenida name={nombreUsuario} onLogout={handleLogout} />
            </div>
          }
        />


        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/creaciones" element={<Creaciones />} />
  <Route path="/perfil" element={<Perfil />} />
  <Route path="/edit-user" element={<EditUser />} />
        <Route path="/misnoticias" element={<MisNoticias />} />
        <Route path="/graficas" element={<Graficas />} /> 
=======
  {/* Ruta de login */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      {/* Ruta para Creaciones */}
      <Route path="/creaciones" element={<Creaciones />} />
      <Route path="/perfil" element={<Perfil />} />
      <Route path="/misnoticias" element={<MisNoticias />} />
      <Route path="/chat/:chatId" element={<Chat />} />
      <Route path="/" element={<App/>}/>

      </Routes>
    </Router>
  );
};

export default App;
