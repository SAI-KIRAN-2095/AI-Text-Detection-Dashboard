import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const analyzeText = async (text, model = "all") => {
  const response = await axios.post(`${API_URL}/predict`, {
    text: text,
    model: model,
  });
  return response.data;
};