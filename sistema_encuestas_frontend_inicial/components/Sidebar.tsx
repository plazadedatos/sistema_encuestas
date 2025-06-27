"use client";

import Link from "next/link";
import { useAuth } from "../context/authContext"; // 👈 Importar el hook

export default function Sidebar() {
  const { logout } = useAuth(); // 👈 Extraer logout del contexto

  return (
    <aside className="w-64 bg-primary text-white min-h-screen flex flex-col justify-between p-6">
      {/* Parte superior: navegación */}
        <div>
        <h2 className="text-xl font-bold mb-6 text-white">Menú</h2>
        <nav className="flex flex-col gap-3 text-base">
            <Link
            href="/panel"
            className="transition-all duration-300 px-4 py-2 rounded-xl text-white hover:bg-blue-800 hover:scale-[1.03] hover:ring-2 hover:ring-white/20"
            >
            Inicio
            </Link>
            <Link
            href="/panel/encuestas"
            className="transition-all duration-300 px-4 py-2 rounded-xl text-white hover:bg-blue-800 hover:scale-[1.03] hover:ring-2 hover:ring-white/20"
            >
            Encuestas
            </Link>
            <Link
            href="/panel/recompensas"
            className="transition-all duration-300 px-4 py-2 rounded-xl text-white hover:bg-blue-800 hover:scale-[1.03] hover:ring-2 hover:ring-white/20"
            >
            Recompensas
            </Link>
            <Link
            href="/panel/misdatos"
            className="transition-all duration-300 px-4 py-2 rounded-xl text-white hover:bg-blue-800 hover:scale-[1.03] hover:ring-2 hover:ring-white/20"
            >
            Mis Datos
            </Link>
            <Link
            href="/panel/historial"
            className="transition-all duration-300 px-4 py-2 rounded-xl text-white hover:bg-blue-800 hover:scale-[1.03] hover:ring-2 hover:ring-white/20"
            >
            Historial
            </Link>
        </nav>
        </div>

      {/* Parte inferior: botón de cerrar sesión */}
      <div>
        <button
          onClick={logout}
          className="transition-all duration-300 px-4 py-2 rounded-xl text-white hover:bg-blue-800 hover:scale-[1.03] hover:ring-2 hover:ring-white/20"
        >
          🔒 Cerrar sesión
        </button>
      </div>
    </aside>
  );
}
