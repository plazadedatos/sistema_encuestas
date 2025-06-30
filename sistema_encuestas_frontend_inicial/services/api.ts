// services/api.ts
import axios from "axios";

// Crea una instancia de Axios
const api = axios.create({
  baseURL: "http://localhost:8000", // 👈 poné aquí tu backend base
  headers: {
    "Content-Type": "application/json",
  },
});

// Opcional: inyectar el token automáticamente si está en localStorage
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
