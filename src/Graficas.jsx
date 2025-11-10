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

  // Cargar comentarios existentes al montar
  useEffect(() => {
    const fetchComentarios = async () => {
      if (!token) return;
      try {
        const res = await fetch(`http://localhost:8000/ws/foro/${foroId}/comentarios`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) {
          const data = await res.json();
          // La API devuelve los comentarios ordenados por fecha desc; invertir para mostrar cronológicamente
          setComentarios(Array.isArray(data) ? data.reverse() : []);
        }
      } catch (e) {
        console.warn('No se pudieron cargar comentarios previos', e);
        setError('No se pudieron cargar los comentarios previos.');
      }
    };
    fetchComentarios();
  }, [foroId, token]);

  useEffect(() => {
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
      // Verificar si el mensaje ya existe por id para evitar duplicados
      setComentarios((prev) => {
        const exists = prev.some(c => c.id_comentario === msg.id_comentario);
        if (exists) return prev;
        return [...prev, msg];
      });
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
  }, [foroId, token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!token || !userId) {
      setError("Solo puedes comentar si has iniciado sesión.");
      return;
    }
    if (!nuevoComentario.trim()) return;

    const mensaje = { contenido: nuevoComentario.trim() };

    try {
      // Si el WebSocket está abierto, usar WebSocket
      if (socketRef.current?.readyState === WebSocket.OPEN) {
        socketRef.current.send(JSON.stringify(mensaje));
        setNuevoComentario('');
        setError('');
        return;
      }

      // Si no hay WebSocket disponible, usar REST como fallback
      const res = await fetch(`http://localhost:8000/ws/foro/${foroId}/comentarios`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(mensaje)
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || res.status);
      }

      // Limpiar input después de envío exitoso
      setNuevoComentario('');
      setError('');
    } catch (err) {
      console.error('Error al enviar comentario:', err);
      setError('Error al enviar el comentario: ' + err.message);
    }
  };

  return (
    <div className="foro-container">
      <h3>Foro de discusión</h3>
      <div className="comentarios-area">
        <div className="comentarios-list">
          {comentarios.length === 0 && (
            <p className="sin-comentarios">Aún no hay comentarios.</p>
          )}
          {comentarios.map((c, index) => (
            <div key={c.id_comentario || index} className="comentario">
              <div className="comentario-header">
                <img 
                  src={c.profile_image || "/img/perfil.svg"} 
                  alt={c.username || `Usuario ${c.id_user}`} 
                  className="user-avatar"
                />
                <strong>{c.username || `Usuario ${c.id_user}`}</strong>
              </div>
              <div className="comentario-content">
                {c.contenido}
              </div>
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
            <ResponsiveContainer width="100%" height={360}>
              <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                <XAxis 
                  dataKey="year" 
                  stroke="#9ca3af"
                  tick={{ fill: '#9ca3af' }}
                />
                <YAxis 
                  stroke="#9ca3af"
                  tick={{ fill: '#9ca3af' }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#2b2b2b',
                    border: '1px solid #444',
                    color: '#fff'
                  }}
                />
                <Legend 
                  wrapperStyle={{
                    color: '#9ca3af'
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="cop_usd"
                  stroke="#00c0ff"
                  strokeWidth={2}
                  dot={{ r: 4 }}
                  name="COP/USD"
                />
                <Line
                  type="monotone"
                  dataKey="cop_eur"
                  stroke="#f1c40f"
                  strokeWidth={2}
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
