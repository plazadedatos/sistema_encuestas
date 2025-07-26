// services/api.ts
import axios, { AxiosError } from "axios";
import { toast } from "react-toastify";

// Configuración de la API
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "");

// Crear instancia de Axios con headers obligatorios
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json', // 👈 Corrección obligatoria para evitar error 500
  },
});

// Log base URL para depuración
console.log("🌐 API base URL:", `${API_BASE_URL}/api`);

// Función para limpiar datos de autenticación
const clearAuthData = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  console.log("🔒 Datos de autenticación eliminados");
};

// Interceptor para requests - agrega token automáticamente
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // Log de la solicitud
    const url = `${config.baseURL || ""}${config.url}`;
    console.log(`➡️  ${config.method?.toUpperCase()} ${url}`);
    console.log(`📦 Request data:`, config.data);
    console.log(`🔧 Request headers:`, config.headers);
    return config;
  },
  (error) => {
    console.error("❌ Error en interceptor de request:", error);
    return Promise.reject(error);
  },
);

// Interceptor para responses - manejo global de errores
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    console.error("❌ API error:", {
      message: error.message,
      status: error.response?.status,
      url: error.config?.url,
    });

    const status = error.response?.status;

    if (status === 401) {
      clearAuthData();
      toast.error("Sesión expirada. Por favor, inicia sesión nuevamente.");
      if (!window.location.pathname.includes("/login")) {
        window.location.href = "/login";
      }
    } else if (status === 403) {
      toast.error("No tienes permisos para realizar esta acción.");
    } else if (status && status >= 500) {
      toast.error("Error del servidor. Intenta nuevamente más tarde.");
    } else if (error.code === "ECONNABORTED") {
      toast.error("La petición tardó demasiado. Verifica tu conexión.");
    } else if (!error.response) {
      toast.error("No se puede conectar al servidor. Verifica tu conexión.");
    }

    return Promise.reject(error);
  },
);

export default api;
