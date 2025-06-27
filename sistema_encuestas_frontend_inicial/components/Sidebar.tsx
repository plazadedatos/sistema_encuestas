"use client";

import Link from "next/link";
import { useAuth } from "../context/authContext"; // 👈 Importar el hook

export default function Sidebar() {
  const { logout } = useAuth(); // 👈 Extraer logout del contexto

  return (
    <aside className="w-64 bg-primary text-white min-h-screen flex flex-col justify-between p-6">
      {/* Parte superior: navegación */}
      <div>
        <h2 className="text-lg font-semibold mb-6">Menú</h2>
        <nav className="flex flex-col gap-4 text-sm">
          <Link href="/panel" className="hover:underline">Inicio</Link>
          <Link href="/panel/encuestas" className="hover:underline">Encuestas</Link>
          <Link href="/panel/recompensas" className="hover:underline">Recompensas</Link>
        </nav>
      </div>

      {/* Parte inferior: botón de cerrar sesión */}
      <div>
        <button
          onClick={logout}
          className="mt-10 text-sm text-white/90 hover:text-red-300 hover:underline transition"
        >
          🔒 Cerrar sesión
        </button>
      </div>
    </aside>
  );
}
