import React from 'react';
import './landing.css';
import logo from './assets/logo-ec.png';

const Landing = ({ onExplore }) => (
  <div className="landing-root">
    <header className="landing-header">
      <div className="header-left">
        <img src={logo} alt="EconoConnect Logo" className="header-logo" />
        <span className="header-title">EconoConnect</span>
      </div>
      <nav className="header-menu">
        <a href="/" className="header-link">Inicio</a>
        <a href="/noticias" className="header-link">Noticias</a>
        <a href="/foro" className="header-link">Foro</a>
        <a href="/login" className="header-link">Login</a>
      </nav>
    </header>
    <section className="landing-hero">
      <img src={logo} alt="EconoConnect Logo" className="hero-logo" />
      <h1 className="hero-title">EconoConnect</h1>
      <p className="hero-slogan">
        Red Social de Economía, donde la educación financiera es para todos,<br />
        para que las personas puedan aprender, compartir y debatir sobre temas financieros<br />
        de forma clara, accesible y segura.
      </p>
      <button className="hero-btn" onClick={onExplore}>Explorar Noticias</button>
    </section>
    {/* El carrusel de noticias se renderiza debajo del hero en App.jsx */}
  </div>
);

export default Landing;
