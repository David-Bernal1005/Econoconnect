import React, { useState, useEffect, useRef } from "react";
import Menu from "./Menu";
import {LineChart,Line,XAxis,YAxis,CartesianGrid,Tooltip,Legend,ResponsiveContainer,} from "recharts";
import "./graficas.css";

function ForoWS({ foroId = 1 }) {
  const [comentarios, setComentarios] = useState([]);
  const [nuevoComentario, setNuevoComentario] = useState("");
  const [error, setError] = useState("");
  const socketRef = useRef(null);

  const userId = localStorage.getItem("user_id");
  const token = localStorage.getItem("token");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("Necesitas iniciar sesión para participar en el foro");
      return;
    }

    const wsUrl = `ws://localhost:8000/ws/foro/${foroId}?token=${token}`;
    console.log("Intentando conectar a:", wsUrl);
    const ws = new WebSocket(wsUrl);
    socketRef.current = ws;

    ws.onopen = () => {
      console.log("Conexión WebSocket establecida");
      setError("");
    };

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.error) {
        setError(msg.error);
        return;
      }
      setComentarios((prev) => [...prev, msg]);
      setError("");
    };

    ws.onclose = (event) => {
      console.log("Conexión WebSocket cerrada", event.code);
      if (event.code === 1008) {
        setError("Necesitas iniciar sesión para participar en el foro");
      }
    };

    ws.onerror = (error) => {
      console.error("Error en WebSocket:", error);
      setError("Error de conexión con el foro");
    };

    return () => {
      if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
        socketRef.current.close();
      }
    };
  }, [foroId]);

  const handleSubmit = (e) => {
    e.preventDefault();

    
    if (!token || !userId) {
      setError("Solo puedes comentar si has iniciado sesión.");
      return;
    }

    if (!nuevoComentario.trim()) return;

    const mensaje = {
      contenido: nuevoComentario.trim(),
    };

    socketRef.current.send(JSON.stringify(mensaje));
    setNuevoComentario("");
    setError(""); 
  };

  return (
    <div className="foro-container">
      <h3>Foro de discusión</h3>
      <div className="comentarios-list">
        {comentarios.length === 0 && (
          <p className="sin-comentarios">Aún no hay comentarios.</p>
        )}
        {comentarios.map((c, index) => (
          <div key={c.id_comentario || index} className="comentario">
            <strong>{c.username || `Usuario ${c.id_user}`}:</strong> {c.contenido}
            {c.fecha_creacion && <span className="fecha">{new Date(c.fecha_creacion).toLocaleString()}</span>}
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

      {error && <p style={{ color: "red", marginTop: "8px" }}>{error}</p>}
    </div>
  );
}

export default function Graficas() {
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/v1/graficas");
        if (!res.ok) throw new Error('Network response was not ok');
        const json = await res.json();
        // Asegurar formato: [{ year, cop_usd, cop_eur }, ...]
        setChartData(json.map((r) => ({ year: r.year, cop_usd: r.cop_usd, cop_eur: r.cop_eur })));
      } catch (e) {
        console.warn('No se pudo cargar datos reales de graficas', e);
        setError('No se pudo obtener datos reales de tasas.');
        setChartData([]);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

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
            {loading && <p>Cargando datos de tasas...</p>}
            {!loading && chartData.length === 0 && (
              <div className="sin-datos" style={{ color: '#f87171' }}>
                <p>{error || 'No hay datos disponibles para mostrar.'}</p>
              </div>
            )}
            <ResponsiveContainer width="100%" height={380}>
              <LineChart data={chartData}>
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

          <ForoWS foroId={1} />
        </div>
      </div>
    </div>
  );
}
