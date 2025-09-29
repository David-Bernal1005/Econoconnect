import { useEffect, useState } from "react";

export default function Inbox({userId, onSelectChat}) {

    const  [chats, setChats] = useState([]);

    useEffect(() => {
    fetch(`http://localhost:8000/api/v1/chats/${userId}`)
      .then((res) => res.json())
      .then(setChats);
    }, [userId]);

    return(
         <div>
      <h2>📩 Mis Chats</h2>
      <ul>
        {chats.map((chat) => (
          <li key={chat.id_chat}>
            <button onClick={() => onSelectChat(chat.id_chat)}>
              <b>{chat.nombre}</b> <br />
              {chat.ultimo_mensaje || "Sin mensajes"}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}