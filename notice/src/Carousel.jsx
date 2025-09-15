// Carrusel.jsx
import React, { useState, useEffect } from 'react';
import Notice from './Notice';
import './carousel.css';  // CSS del carrusel que ya tienes

const slides = [
    {
    id: 0,
    component: <Notice />  // Aquí va tu componente Notice directamente
    },
    {
    id: 1,
    component: <Notice />  // Aquí va tu componente Notice directamente
    },
    {
    id: 2,
    component: <Notice />  // Aquí va tu componente Notice directamente
    },
    {
    id: 3,
    component: <Notice />  // Aquí va tu componente Notice directamente
    },
    {
    id: 4,
    component: <Notice />  // Aquí va tu componente Notice directamente
    },
];


export default function Carousel() {
    const [current, setCurrent] = useState(0);
    const slideWidth = 25; // % por slide
    const offset = (100 - slideWidth) / 2; // desplazamiento para centrar

  // Recalcular el desplazamiento cuando el componente se monta
    useEffect(() => {
    setCurrent(Math.floor(slides.length / 2)); // Centrar el primer slide
    }, []);

    const prevSlide = () => {
    setCurrent(current === 0 ? slides.length - 1 : current - 1);
    };

    const nextSlide = () => {
    setCurrent(current === slides.length - 1 ? 0 : current + 1);
    };

    return (
    <div className="carousel">
        <div
        className="slides"
        style={{
          transform: `translateX(-${(current * slideWidth) - offset}%)`,
            display: 'flex',
            transition: 'transform 0.5s ease-in-out',
        }}
        >
        {slides.map((slide, index) => {
          // Cálculo de la escala
            const isCurrent = index === current;
            const isPrev = index === (current === 0 ? slides.length - 1 : current - 1);
            const isNext = index === (current === slides.length - 1 ? 0 : current + 1);

            const scale = isCurrent ? 1.1 : isPrev || isNext ? 0.9 : 1.1;

            return (
            <div
                key={slide.id}
                className="slide"
                style={{
                minWidth: `${slideWidth}%`,
                boxSizing: 'border-box',
                transform: `scale(${scale})`, // Aplicamos la escala
                transition: 'transform 0.5s ease-in-out', // Efecto suave de transición
                }}
            >
                {slide.component}
            </div>
            );
        })}
        </div>

        <div className="botones">
        <button className="boton" onClick={prevSlide}>
            &#10096;
        </button>
        <button className="boton" onClick={nextSlide}>
            &#10097;
        </button>
        </div>
    </div>
    );
}
