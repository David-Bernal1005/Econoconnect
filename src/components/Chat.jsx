import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';

const Chat = ({ chatId, usuario }) => {
    const [mensajes, setMensajes] = useState([]);
    const [nuevoMensaje, setNuevoMensaje] = useState('');
    const [miembros, setMiembros] = useState([]);
    const [error, setError] = useState(null);
    const webSocketRef = useRef(null);
    const mensajesRef = useRef(null);

    // Conectar al WebSocket
    useEffect(() => {
        // Crear conexión WebSocket
        webSocketRef.current = new WebSocket(`ws://localhost:8000/ws/chat/${chatId}`);

        webSocketRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMensajes(prev => [...prev, data]);
        };

        webSocketRef.current.onclose = () => {
            console.log('WebSocket desconectado');
        };

        webSocketRef.current.onerror = (error) => {
            console.error('Error en WebSocket:', error);
            setError('Error de conexión');
        };

        // Cargar mensajes anteriores
        cargarMensajesAnteriores();
        // Cargar miembros del chat
        cargarMiembros();

        return () => {
            if (webSocketRef.current) {
                webSocketRef.current.close();
            }
        };
    }, [chatId]);

    // Auto-scroll a los mensajes nuevos
    useEffect(() => {
        if (mensajesRef.current) {
            mensajesRef.current.scrollTop = mensajesRef.current.scrollHeight;
        }
    }, [mensajes]);

    const cargarMensajesAnteriores = async () => {
        try {
            const response = await fetch(`/api/v1/chats/${chatId}/mensajes`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setMensajes(data);
        } catch (error) {
            console.error('Error al cargar mensajes:', error);
            setError('Error al cargar mensajes anteriores');
        }
    };

    const cargarMiembros = async () => {
        try {
            const response = await fetch(`/api/v1/chats/${chatId}/miembros`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            const data = await response.json();
            setMiembros(data);
        } catch (error) {
            console.error('Error al cargar miembros:', error);
        }
    };

    const enviarMensaje = (e) => {
        e.preventDefault();
        if (!nuevoMensaje.trim()) return;

        const mensaje = {
            id_user: usuario.id_user,
            contenido: nuevoMensaje,
            fecha_envio: new Date().toISOString()
        };

        webSocketRef.current.send(JSON.stringify(mensaje));
        setNuevoMensaje('');
    };

    return (
        <div className="chat-container">
            {error && <div className="error-message">{error}</div>}
            
            <div className="chat-sidebar">
                <h3>Miembros</h3>
                <ul className="miembros-lista">
                    {miembros.map(miembro => (
                        <li key={miembro.id_user} className="miembro-item">
                            <span>{miembro.nombre}</span>
                            <span className="rol-badge">{miembro.rol_chat}</span>
                        </li>
                    ))}
                </ul>
            </div>

            <div className="chat-main">
                <div className="mensajes-container" ref={mensajesRef}>
                    {mensajes.map((mensaje, index) => (
                        <div
                            key={index}
                            className={`mensaje ${mensaje.id_user === usuario.id_user ? 'mensaje-propio' : 'mensaje-otro'}`}
                        >
                            <div className="mensaje-contenido">{mensaje.contenido}</div>
                            <div className="mensaje-info">
                                <span className="mensaje-autor">{mensaje.nombre_usuario}</span>
                                <span className="mensaje-hora">
                                    {new Date(mensaje.fecha_envio).toLocaleTimeString()}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>

                <form onSubmit={enviarMensaje} className="mensaje-form">
                    <input
                        type="text"
                        value={nuevoMensaje}
                        onChange={(e) => setNuevoMensaje(e.target.value)}
                        placeholder="Escribe un mensaje..."
                        className="mensaje-input"
                    />
                    <button type="submit" className="enviar-btn">
                        Enviar
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Chat;