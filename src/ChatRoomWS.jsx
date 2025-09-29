import { useEffect, useState, useRef } from "react";

export default function ChatRoomWS({ chatId, userId, onBack }) {
  const [messages, setMessages] = useState([]);
  const [content, setContent] = useState("");
  const socketRef = useRef(null);

  useEffect(() => {
    socketRef.current = new WebSocket(`ws://localhost:8000/ws/chat/${chatId}`);

    socketRef.current.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      setMessages((prev) => [...prev, msg]);
    };

    return () => socketRef.current.close();
  }, [chatId]);

  const handleSend = () => {
    if (!content.trim()) return;
    socketRef.current.send(JSON.stringify({
      id_user: userId,
      contenido: content
    }));
    setContent("");
  };

  return (
    <div>
      <button onClick={onBack}>⬅ Volver</button>
      <h2>Chat {chatId}</h2>
      <div className="messages">
        {messages.map((msg) => (
          <p key={msg.id_mensaje}>
            <b>Usuario {msg.id_user}:</b> {msg.contenido}
          </p>
        ))}
      </div>
      <input
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Escribe un mensaje..."
      />
      <button onClick={handleSend}>Enviar</button>
    </div>
  );
}
