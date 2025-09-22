import React from 'react';
import { Link } from "react-router-dom";
import './menu.css';    

const Menu = () => {
    return (
        <div className="slidebar">
            <ul>
                <Link to="">
                    <img src="img/perfil.svg" alt="Perfil"/>
                    <span>perfil</span>
                </Link>
            </ul>
            <ul>
                <Link to="/">
                    <img src="img/inicio.svg" alt="Inicio"/>
                    <span>Inicio</span>
                </Link>
            </ul>
            <ul>
                <Link to="">
                    <img src="img/chats.svg" alt="Chats"/>
                    <span>Chats</span>
                </Link>
            </ul>
            <ul>
                <Link to="">
                    <img src="img/graficos.svg" alt="Graficos"/>
                    <span>Graficos</span>
                </Link>
            </ul>
            <ul>
                <Link to="/creaciones">
                    <img src="img/creaciones.svg" alt="Creaciones"/>
                    <span>Creaciones</span>
                </Link>
            </ul>
        </div>
    );
};

export default Menu;