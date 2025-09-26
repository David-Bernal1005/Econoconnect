import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getMessages, sendMessage } from "./services/menssageService";

export default function ChatRoom() {
  const { chatId } = useParams();
  const userId = 1; // Placeholder, replace with actual user ID from auth
  const [messages, setMessages] = useState([]);
  const [content, setContent] = useState("");

  useEffect(() => {
    loadMessages();
  }, [chatId]);

  const loadMessages = async () => {
    const data = await getMessages(chatId);
    setMessages(data);
  };

  const handleSend = async () => {
    if (!content.trim()) return;
    await sendMessage({ id_chat: chatId, id_user: userId, contenido: content });
    setContent("");
    loadMessages();
  };

  return (
    <div>
      <h2>Chat {chatId}</h2>
      <div className="messages">
        {messages.map((msg) => (
          <p key={msg.id_mensaje}>
            <b>Usuario {msg.id_user}:</b> {msg.contenido} <i>({msg.estado})</i>
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
