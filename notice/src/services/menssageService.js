import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL + "/chat_mensaje";

export const sendMessage = async (message) => {
  const res = await axios.post(API_URL + "/", message);
  return res.data;
};

export const getMessages = async (chatId) => {
  const res = await axios.get(`${API_URL}/${chatId}`);
  return res.data;
};