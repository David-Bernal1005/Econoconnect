import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";

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
import Graficas from "./Graficas"; 
import Inbox from "./Inbox";
import ChatRoomWS from "./ChatRoomWS";
import EditUser from "./EditUser";



import "./app.css";

const App = () => {
  // Detectar ruta actual para ocultar el botón en /login
  function LoginButton() {
    const location = useLocation();
    const isLogged = Boolean(localStorage.getItem("token"));
  if (!isLogged && location.pathname !== "/login" && location.pathname !== "/register") {
      return (
        <a href="/login" style={{
          position: "fixed",
          top: 20,
          right: 20,
          zIndex: 1000,
          background: "#222",
          borderRadius: "50px",
          padding: "8px 24px",
          color: "#FFD600",
          fontWeight: "bold",
          boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
          textDecoration: "none",
          display: "flex",
          alignItems: "center"
        }}>
          <img src="/img/exit.svg" alt="Login" style={{ width: 28, height: 28, marginRight: 8 }} />
          Login
        </a>
      );
    }
    return null;
  }
  const [match, setMatch] = useState(false);
  const [searching, setSearching] = useState(false);
  const [noticias, setNoticias] = useState([]);
  const [nombreUsuario, setNombreUsuario] = useState(
    localStorage.getItem("nombre_usuario")
  );
  const [selectedChat, setSelectedChat] = useState(null);
  const userId = localStorage.getItem("user_id") ? parseInt(localStorage.getItem("user_id")) : 1;

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
    localStorage.removeItem("user_id");
    setNombreUsuario("");
    window.location.href = "/";
  };

  const isLogged = Boolean(localStorage.getItem("token"));

  return (
    <Router>
      <LoginButton />
      <Routes>
        <Route
          path="/"
          element={
            <div className="main-layout">
              <aside>
                {isLogged && <Menu />}
                {isLogged && <Exit />}
                {/* Filter desactivado temporalmente */}
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
        <Route path="login/forgot-password" element={<ForgotPassword />} />
        <Route path="/creaciones" element={<Creaciones />} />
        <Route path="/perfil" element={<Perfil />} />
        <Route path="/edit-user" element={<EditUser />} />
        <Route path="/misnoticias" element={<MisNoticias />} />
        <Route path="/graficas" element={<Graficas />} /> 

        <Route
          path="/chat"
          element={
            !selectedChat ? (
              <Inbox userId={userId} onSelectChat={setSelectedChat} />
            ) : (
              <ChatRoomWS
                chatId={selectedChat}
                userId={userId}
                onBack={() => setSelectedChat(null)}
              />
            )
          }
        />


      {/*<Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/creaciones" element={<Creaciones />} />
      <Route path="/perfil" element={<Perfil />} />
      <Route path="/misnoticias" element={<MisNoticias />} />
      <Route path="/chat/:chatId" element={<Chat />} />
      <Route path="/" element={<App/>}/>*/}
      </Routes>
     </Router>
  );
};

export default App;
