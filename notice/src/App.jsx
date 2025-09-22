import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Menu from "./Menu";
import Login from "./Login"; 
import Search from "./Search";
import Exit from "./Exit";
import Carousel from "./Carousel";
import Notice from "./Notice";
import Filter from "./Filter";
import Register from "./register";
import Creaciones from "./Creaciones";



import "./app.css";
import { noticeData } from "./data";

const App = () => {
  const [match, setMatch] = useState(false);
  const [searching, setSearching] = useState(false);

  const handleSearch = (result) => {
    setMatch(result.match);
    setSearching(result.searching);
  };

  return (
    <Router>
      <Routes>
        {/* Ruta principal con tu layout */}
        <Route
          path="/"
          element={
            <div className="main-layout">
              <aside>
                <Menu />
                <Exit />
                <Filter />
              </aside>
              <div className="main-content">
                <Search onSearch={handleSearch} />
                <section className="content-section">
                  {searching ? (match ? <Notice /> : null) : <Carousel />}
                </section>
              </div>
            </div>
          }
        />

        {/* Ruta de login */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        {/* Ruta para Creaciones */}
        <Route path="/creaciones" element={<Creaciones />} />
      </Routes>
    </Router>
  );
};

export default App;
