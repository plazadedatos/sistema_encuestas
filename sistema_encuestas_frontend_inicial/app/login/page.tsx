// app/login/page.tsx
"use client";
import { useState } from "react";
import { useAuth } from "../../context/authContext";

export default function LoginPage() {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    const success = login(username, password);
    if (!success) setError("Credenciales inválidas");
  };

  return (
    <section className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleLogin} className="bg-white shadow-md p-8 rounded-lg w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-4">Iniciar sesión</h2>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        <input
          type="text"
          placeholder="Usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-4 p-2 border rounded"
        />
        <button className="bg-primary text-white w-full py-2 rounded hover:bg-primary-dark">
          Entrar
        </button>
      </form>
    </section>
  );
}
