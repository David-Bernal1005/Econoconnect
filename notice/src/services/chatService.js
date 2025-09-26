import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL + "/chat";

export const createChat = async (chat) => {
  const res = await axios.post(API_URL + "/", chat);
  return res.data;
};

export const getChatsByUser = async (userId) => {
  const res = await axios.get(`${API_URL}/usuario/${userId}`);
  return res.data;
};