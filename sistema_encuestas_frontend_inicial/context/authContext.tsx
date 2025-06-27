// ✅ PASO 1: Crear archivo authContext.tsx en carpeta context
"use client"; // 👈 DEBE IR COMO PRIMERA LÍNEA
import { createContext, useContext, useState, useEffect } from "react";
import { useRouter } from "next/navigation";

interface AuthContextProps {
  isAuthenticated: boolean;
  login: (username: string, password: string) => boolean;
  logout: () => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const auth = localStorage.getItem("auth");
    if (auth === "true") setIsAuthenticated(true);
  }, []);

  const login = (username: string, password: string) => {
    if (username === "admin" && password === "123") {
      localStorage.setItem("auth", "true");
      setIsAuthenticated(true);
      router.push("/panel");
      return true;
    }
    return false;
  };

  const logout = () => {
    localStorage.removeItem("auth");
    setIsAuthenticated(false);
    router.push("/");
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth debe usarse dentro de AuthProvider");
  return context;
};
