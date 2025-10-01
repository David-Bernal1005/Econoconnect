import React, { useState, useEffect } from 'react';
import Notice from './Notice';
import './carousel.css';

export default function Carousel() {
    const [noticias, setNoticias] = useState([]);
    const [current, setCurrent] = useState(0);

    useEffect(() => {
        fetch('http://localhost:8000/api/v1/noticias')
            .then(res => {
                if (!res.ok) throw new Error('No se pudo cargar noticias: ' + res.status);
                return res.json();
            })
            .then(data => {
                if (!Array.isArray(data)) {
                    setNoticias([]);
                    console.error('La respuesta de noticias no es un array:', data);
                } else {
                    // Ordena por fecha_publicacion descendente (más nueva primero)
                    const ordenadas = [...data].sort((a, b) => new Date(b.fecha_publicacion) - new Date(a.fecha_publicacion));
                    setNoticias(ordenadas);
                    // Centra la más nueva (primera en el array ordenado)
                    if (ordenadas.length > 0) {
                        setCurrent(0);
                    }
                }
            })
            .catch(err => {
                console.error('Error al cargar noticias:', err);
                setNoticias([]);
            });
    }, []);

    if (!Array.isArray(noticias) || noticias.length === 0) {
        return (
            <div style={{ color: '#fff', textAlign: 'center', padding: '2rem', background: '#23262b', minHeight: '70vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                No hay noticias disponibles.<br />
                Revisa la consola para más detalles.<br />
                {typeof noticias === 'string' ? noticias : null}
            </div>
        );
    }

    // Mostrar 3 noticias con escala animada
    const getVisibleNoticias = () => {
        if (!Array.isArray(noticias)) return [];
        if (noticias.length <= 3) {
            // Si hay 3 o menos, la central es la del medio
            return noticias.map((n, i) => ({ noticia: n, idx: i }));
        }
        // Siempre el centro visual es el primer del array visible
        const izquierda = current === 0 ? noticias.length - 1 : current - 1;
        const derecha = (current + 1) % noticias.length;
        // Orden: izquierda, centro, derecha
        return [
            { noticia: noticias[izquierda], idx: izquierda },
            { noticia: noticias[current], idx: current },
            { noticia: noticias[derecha], idx: derecha }
        ];
    };

    const prevSlide = () => {
        setCurrent(current === 0 ? noticias.length - 1 : current - 1);
    };
    const nextSlide = () => {
        setCurrent((current + 1) % noticias.length);
    };

    return (
        <div className="main-content">
            <div className="carousel" style={{ width: '80vw', height: '60vh', borderRadius: '10px', background: 'transparent', display: 'flex', alignItems: 'center', justifyContent: 'center', boxSizing: 'border-box', position: 'relative' }}>
                <div
                    className="slides"
                    style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        width: '100%',
                        gap: '2rem',
                        transition: 'transform 0.5s ease-in-out',
                    }}
                >
                    {getVisibleNoticias().map(({ noticia, idx }, pos) => {
                        if (!noticia) return null;
                        // Animación de movimiento igual para izquierda y derecha
                        let baseScale = pos === 1 ? 1.35 : 0.8;
                        let translateX = (pos === 0 || pos === 2) ? '-220px' : '0px';
                        if (pos === 2) translateX = '220px'; // Para mantener la dirección
                        let zIndex = pos === 1 ? 2 : 1;
                        let opacity = pos === 1 ? 1 : 0.5;
                        let boxShadow = pos === 1 ? '0 8px 32px rgba(0,0,0,0.18)' : '0 2px 12px rgba(0,0,0,0.10)';
                        let transition = 'transform 0.6s cubic-bezier(.4,1.4,.6,1), opacity 0.4s';
                        // Si es derecha, usa exactamente la misma animación que la izquierda
                        if (pos === 2) {
                            baseScale = 0.8;
                            translateX = '220px';
                            transition = 'transform 0.6s cubic-bezier(.4,1.4,.6,1), opacity 0.4s';
                        }
                        if (pos === 0) {
                            baseScale = 0.8;
                            translateX = '-220px';
                            transition = 'transform 0.6s cubic-bezier(.4,1.4,.6,1), opacity 0.4s';
                        }
                        let style = {
                            minWidth: '32%',
                            maxWidth: '34%',
                            marginLeft: pos === 0 ? '2vw' : undefined,
                            marginRight: pos === 2 ? '2vw' : undefined,
                            boxSizing: 'border-box',
                            display: 'flex',
                            justifyContent: 'center',
                            alignItems: 'center',
                            transform: `scale(${baseScale}) translateX(${translateX})`,
                            transition: transition,
                            opacity: opacity,
                            zIndex: zIndex,
                            boxShadow: boxShadow,
                        };
                        return (
                            <div
                                key={noticia.id || idx}
                                className="slide"
                                style={style}
                            >
                                <Notice noticia={noticia} />
                            </div>
                        );
                    })}
                </div>
                <div className="botones" style={{
                    position: 'absolute',
                    top: '50%',
                    left: 0,
                    width: '100%',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    pointerEvents: 'none',
                    zIndex: 10
                }}>
                    <button className="boton" onClick={prevSlide} style={{
                        pointerEvents: 'auto',
                        position: 'absolute',
                        right: '75%',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        width: '38px',
                        height: '38px',
                        fontSize: '2rem',
                        borderRadius: '20%',
                        background: '#f1c40f',
                        boxShadow: '0 2px 8px rgba(0,0,0,0.12)',
                        border: 'none',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                    }}>
                        &#10096;
                    </button>
                    <button className="boton" onClick={nextSlide} style={{
                        pointerEvents: 'auto',
                        position: 'absolute',
                        left: '75%',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        width: '38px',
                        height: '38px',
                        fontSize: '2rem',
                        borderRadius: '20%',
                        background: '#f1c40f',
                        boxShadow: '0 2px 8px rgba(0,0,0,0.12)',
                        border: 'none',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                    }}>
                        &#10097;
                    </button>
                </div>
            </div>
        </div>
    );
}
