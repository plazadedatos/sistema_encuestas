"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";

interface AuthContextType {
  isAuthenticated: boolean;
  user: any;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);

  // ✅ Al iniciar, decodifica token y mapea rol_id => rol
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const decoded: any = jwtDecode(token);
        console.log("🟢 Token cargado al iniciar sesión:", decoded);

        const usuario = {
          ...decoded,
          rol: decoded.rol_id, // ✅ normalizamos el campo
        };

        setUser(usuario);
      } catch (err) {
        console.error("❌ Token inválido", err);
        localStorage.removeItem("token");
      }
    }
  }, []);

  // ✅ Login: guarda token y mapea rol_id => rol
  const login = async (email: string, password: string) => {
    try {
      const res = await fetch("http://localhost:8000/auth/login", {

        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) return false;

      const data = await res.json();
      const decoded: any = jwtDecode(data.access_token);
      console.log("🟢 Token recibido en login:", decoded);

      const usuario = {
        ...decoded,
        rol: decoded.rol_id, // ✅ normalizamos el campo
      };

      setUser(usuario);
      localStorage.setItem("token", data.access_token);
      router.push("/panel");
      return true;
    } catch (err) {
      console.error("❌ Error en login:", err);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!user,
        user,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext)!;
