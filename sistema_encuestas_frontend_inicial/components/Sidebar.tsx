"use client";

import Link from "next/link";
import { useState } from "react";
import { useAuth } from "@/context/authContext";
import { FaBars, FaChevronDown, FaChevronUp, FaHome, FaPoll, FaGift, FaUser, FaHistory, FaTools } from "react-icons/fa";

export default function Sidebar() {
  const { logout, user } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [adminOpen, setAdminOpen] = useState(false);

  return (
    <>
      {/* Botón para abrir/cerrar en mobile */}
      <button
        onClick={() => setMenuOpen(!menuOpen)}
        className="md:hidden fixed top-4 left-4 z-50 text-white bg-blue-700 p-2 rounded"
      >
        <FaBars />
      </button>

      {/* Sidebar */}
      <aside
        className={`bg-gradient-to-b from-blue-800 to-blue-600 text-white w-64 fixed top-0 left-0 h-full p-6 transition-transform duration-300 z-40 ${
          menuOpen ? "translate-x-0" : "-translate-x-full"
        } md:translate-x-0 md:static md:flex md:flex-col md:min-h-screen`}
      >
        {/* Título */}
        <h2 className="text-2xl font-bold mb-6">Menú</h2>
        <nav className="flex flex-col gap-3 text-base">
          <Link href="/panel" className="flex items-center gap-2 hover:bg-blue-700 p-2 rounded">
            <FaHome /> Inicio
          </Link>
          <Link href="/panel/encuestas" className="flex items-center gap-2 hover:bg-blue-700 p-2 rounded">
            <FaPoll /> Encuestas
          </Link>
          <Link href="/panel/recompensas" className="flex items-center gap-2 hover:bg-blue-700 p-2 rounded">
            <FaGift /> Recompensas
          </Link>
          <Link href="/panel/misdatos" className="flex items-center gap-2 hover:bg-blue-700 p-2 rounded">
            <FaUser /> Mis Datos
          </Link>
          <Link href="/panel/historial" className="flex items-center gap-2 hover:bg-blue-700 p-2 rounded">
            <FaHistory /> Historial
          </Link>

          {/* Submenú Administración */}
          {(user?.rol === 1 || user?.rol === 2) && (
            <div>
              <button
                onClick={() => setAdminOpen(!adminOpen)}
                className="w-full flex items-center justify-between hover:bg-green-700 p-2 rounded"
              >
                <span className="flex items-center gap-2">
                  <FaTools /> Administración
                </span>
                {adminOpen ? <FaChevronUp /> : <FaChevronDown />}
              </button>
              {adminOpen && (
                <div className="ml-6 mt-2 flex flex-col gap-2">
                  <Link href="/administracion/encuestas" className="flex items-center gap-2 hover:bg-blue-700 p-1 rounded">
                    Encuestas
                  </Link>
                  <Link href="/administracion/recompensas" className="flex items-center gap-2 hover:bg-blue-700 p-1 rounded">
                    Recompensas
                  </Link>
                </div>
              )}
            </div>
          )}
        </nav>

        {/* Cierre sesión */}
        <div className="mt-auto pt-6">
          <button
            onClick={logout}
            className="w-full bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded"
          >
            🔒 Cerrar sesión
          </button>
        </div>
      </aside>
    </>
  );
}
