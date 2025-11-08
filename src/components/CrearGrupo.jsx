import React, { useState, useEffect } from 'react';
import './CrearGrupo.css';

const CrearGrupo = ({ onGrupoCreado }) => {
    const [formData, setFormData] = useState({
        nombre: '',
        descripcion: '',
        visibilidad: 'publico'
    });
    const [error, setError] = useState(null);
    const [esAdmin, setEsAdmin] = useState(false);

    // Verificar si el usuario es administrador
    useEffect(() => {
        const checkAdminStatus = async () => {
            try {
                const response = await fetch('/api/v1/user/roles', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                const data = await response.json();
                setEsAdmin(data.roles.includes('administrador'));
            } catch (error) {
                console.error('Error al verificar rol:', error);
            }
        };
        
        checkAdminStatus();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        try {
            const response = await fetch('/api/v1/grupos/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error al crear el grupo');
            }

            const nuevoGrupo = await response.json();
            onGrupoCreado(nuevoGrupo);
            
            // Limpiar el formulario
            setFormData({
                nombre: '',
                descripcion: '',
                visibilidad: 'publico'
            });
        } catch (error) {
            setError(error.message);
        }
    };

    return (
        <div className="crear-grupo-container">
            <h2>Crear Nuevo Grupo</h2>
            {error && <div className="error-message">{error}</div>}
            
            <form onSubmit={handleSubmit} className="crear-grupo-form">
                <div className="form-group">
                    <label htmlFor="nombre">Nombre del Grupo:</label>
                    <input
                        type="text"
                        id="nombre"
                        name="nombre"
                        value={formData.nombre}
                        onChange={handleChange}
                        required
                        maxLength={100}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="descripcion">Descripción:</label>
                    <textarea
                        id="descripcion"
                        name="descripcion"
                        value={formData.descripcion}
                        onChange={handleChange}
                        rows={4}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="visibilidad">Visibilidad:</label>
                    <select
                        id="visibilidad"
                        name="visibilidad"
                        value={formData.visibilidad}
                        onChange={handleChange}
                        disabled={!esAdmin && formData.visibilidad === 'privado'}
                    >
                        <option value="publico">Público</option>
                        {esAdmin && <option value="privado">Privado</option>}
                    </select>
                </div>

                <button type="submit" className="crear-grupo-btn">
                    Crear Grupo
                </button>
            </form>
        </div>
    );
};

export default CrearGrupo;