import React, { useState } from "react";
import Menu from "./Menu";
import {LineChart,Line,XAxis,YAxis,CartesianGrid,Tooltip,Legend,ResponsiveContainer,} from "recharts";
import "./graficas.css";

const data = [
    { year: "2018", cop_usd: 2976.5, cop_eur: 3675.59 },
    { year: "2019", cop_usd: 3357.6, cop_eur: 3788.65 },
    { year: "2020", cop_usd: 3688.67, cop_eur: 4183.67 },
    { year: "2021", cop_usd: 3830.49, cop_eur: 4392.5 },
    { year: "2022", cop_usd: 4392.5, cop_eur: 4392.5 },
    { year: "2023", cop_usd: 3977.57, cop_eur: 4275.26 },
    { year: "2024", cop_usd: 4081.12, cop_eur: 4409.81 },
    { year: "2025", cop_usd: 4130.27, cop_eur: 4621.17 },
];

function Foro() {
    const [comentarios, setComentarios] = useState([
        { id: 1, usuario: "Ana", contenido: "Muy interesante la gráfica." },
        { id: 2, usuario: "Carlos", contenido: "Podrían agregar más datos." },
    ]);
    const [nuevoComentario, setNuevoComentario] = useState(""); 
    const handleSubmit = (e) => {
        e.preventDefault();
        if (!nuevoComentario.trim()) return;  
        const nuevo = {
            id: comentarios.length + 1,
            usuario: "Usuario", 
            contenido: nuevoComentario.trim(),
        };
        setComentarios([...comentarios, nuevo]);
        setNuevoComentario("");
    };  
    return (
        <div className="foro-container">
            <h3>Foro de discusión</h3>
            <div className="comentarios-list">
                {comentarios.map((c) => (
                    <div key={c.id} className="comentario">
                        <strong>{c.usuario}:</strong> {c.contenido}
                    </div>
                ))}
            </div>
            <form onSubmit={handleSubmit} className="comentario-form">
                <textarea
                    rows={3}
                    value={nuevoComentario}
                    onChange={(e) => setNuevoComentario(e.target.value)}
                    placeholder="Escribe tu comentario..."
                />
                <button type="submit">Enviar</button>
            </form>
        </div>
    );
}

export default function Graficas() {
    return (
        <div className="graficas-page">
            <Menu />
            <div className="graficas-content">
                <div className="graficas-header">
                    <h2>Gráficas</h2>
                </div>
                <div className="monedas">
                    <div className="moneda-card">
                        <img src="/img/cop.png" alt="COP" />
                        <span>COP</span>
                    </div>
                    <div className="moneda-card">
                        <img src="/img/usd.png" alt="USD" />
                        <span>USD</span>
                    </div>
                    <div className="moneda-card">
                        <img src="/img/eur.png" alt="EUR" />
                        <span>EUR</span>
                    </div>
                </div>
                <div className="graficas-main">
                    <div className="chart-container">
                        <ResponsiveContainer width="100%" height={380}>
                            <LineChart data={data}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#2b2b2b" />
                                <XAxis dataKey="year" stroke="#9ca3af" />
                                <YAxis stroke="#9ca3af" />
                                <Tooltip />
                                <Legend />
                                <Line
                                    type="monotone"
                                    dataKey="cop_usd"
                                    stroke="#00c0ff"
                                    dot={{ r: 4 }}
                                    name="COP/USD"
                                />
                                <Line
                                    type="monotone"
                                    dataKey="cop_eur"
                                    stroke="#f1c40f"
                                    dot={{ r: 4 }}
                                    name="COP/EUR"
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                    <Foro />
                </div>
            </div>
        </div>
    );
}
