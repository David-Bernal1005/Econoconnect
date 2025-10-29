import { useEffect, useState } from "react";
import "./inbox.css";

export default function Inbox({ userId, onSelectChat }) {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8000/api/v1/chats/${userId}`)
      .then((res) => res.json())
      .then(setChats)
      .catch(() => setChats([]));
  }, [userId]);

  return (
    <div className="box">
      <h2 className="box-title">📩 Chats</h2>


        <ul className="inbox-list">
          {chats.map((chat) => (
            <li key={chat.id_chat} className="inbox-item">
              <button className="inbox-button" onClick={() => onSelectChat(chat.id_chat)}>
                <div className="avatar">
                  <img src="/img/perfil.svg" alt="avatar" />
                </div>
                <div className="inbox-meta">
                  <div className="inbox-name">{chat.nombre}</div>
                  <div className="inbox-last">{chat.ultimo_mensaje || "Sin mensajes"}</div>
                </div>
              </button>
            </li>
          ))}
        </ul>
      
    </div>
  );
}