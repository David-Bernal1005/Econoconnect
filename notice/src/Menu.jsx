import React from 'react';
import './menu.css';    

const Menu = () => {
    return (
        <div class="slidebar">
            <ul>
                <a href="">
                    <img src="img/perfil.svg" alt="Perfil"/>
                    <span>perfil</span>

                </a>
            </ul>
            <ul>
                <a href="">
                    <img src="img/inicio.svg" alt="Inicio"/>
                    <span>Inicio</span>
                </a>
            </ul>
            <ul>
                <a href="">
                    <img src="img/chats.svg" alt="Chats"/>
                    <span>Chats</span>
                </a>
            </ul>
            <ul>
                <a href="">
                    <img src="img/graficos.svg" alt="Graficos"/>
                    <span>Graficos</span>
                </a>
            </ul>
            <ul>
                <a href="">
                    <img src="img/creaciones.svg" alt="Creaciones"/>
                    <span>Creaciones</span>
                </a>
            </ul>
        </div>
    );
};

export default Menu;