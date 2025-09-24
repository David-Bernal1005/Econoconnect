import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Menu from "./Menu";
import Bienvenida from "./Bienvenida";
import Login from "./Login"; 
import Search from "./Search";
import Exit from "./Exit";
import Carousel from "./Carousel";
import Notice from "./Notice";
import Filter from "./Filter";
import Register from "./register";
import Creaciones from "./Creaciones";
import MisNoticias from "./MisNoticias";



import "./app.css";
import { noticeData } from "./data";

const App = () => {
  const [match, setMatch] = useState(false);
  const [searching, setSearching] = useState(false);

  const handleSearch = (result) => {
    setMatch(result.match);
    setSearching(result.searching);
  };

  const [nombreUsuario, setNombreUsuario] = useState(localStorage.getItem("nombre_usuario"));

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("nombre_usuario");
    setNombreUsuario("");
    window.location.href = "/";
  };

  React.useEffect(() => {
    setNombreUsuario(localStorage.getItem("nombre_usuario"));
  }, []);

  const isLogged = Boolean(localStorage.getItem("token"));

  return (
    <Router>
      <Routes>
        <Route path="/misnoticias" element={<MisNoticias />} />
        <Route
          path="/"
          element={
            <div className="main-layout">
              <aside>
                {isLogged && <Menu />}
                {isLogged && <Exit />}
                {isLogged && <Filter />}
                {!isLogged && (
                  <a href="/login" className="back-link" style={{position: 'fixed', top: 30, right: 30, zIndex: 9999, background: '#ffcc00', color: '#1c2120', padding: '10px 20px', borderRadius: '8px', fontWeight: 'bold', textDecoration: 'none'}}>Login</a>
                )}
              </aside>
              <div className="main-content">
                <Search onSearch={handleSearch} />
                <section className="content-section">
                  {searching ? (match ? <Notice /> : null) : <Carousel />}
                </section>
              </div>
              <Bienvenida name={nombreUsuario} onLogout={handleLogout} />
            </div>
          }
        />

        {/* Ruta de login */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        {/* Ruta para Creaciones */}
        <Route path="/creaciones" element={<Creaciones />} />
        <Route path="/" element={<App/>}/>
      </Routes>
    </Router>
    
  );
};

export default App;
