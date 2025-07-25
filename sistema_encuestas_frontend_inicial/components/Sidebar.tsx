"use client";

import Link from "next/link";
import { useState } from "react";
import { useAuth } from "@/context/authContext";
import Image from "next/image";
import { FaBars, FaChevronDown, FaChevronUp, FaHome, FaPoll, FaGift, FaUser, FaHistory, FaTools, FaChartBar, FaTimes, FaSignOutAlt, FaCog } from "react-icons/fa";

export default function Sidebar() {
  const { logout, user } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [adminOpen, setAdminOpen] = useState(false);

  return (
    <>
      {/* Botón para abrir/cerrar en mobile - Mejorado */}
      <button
        onClick={() => setMenuOpen(true)}
        className="md:hidden fixed top-4 left-4 z-50 bg-gradient-to-r from-brand-vibrant to-brand-medium p-3 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300"
      >
        <FaBars className="text-xl text-white" />
      </button>

      {/* Overlay para mobile con animación */}
      {menuOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black bg-opacity-60 z-30 backdrop-blur-sm transition-opacity duration-300"
          onClick={() => setMenuOpen(false)}
        />
      )}

      {/* Sidebar - Rediseñado con nueva paleta */}
      <aside
        className={`bg-gradient-to-b from-brand-dark via-brand-vibrant to-brand-medium text-white w-72 fixed inset-y-0 left-0 flex flex-col shadow-2xl transition-transform duration-300 ease-in-out z-40 ${
          menuOpen ? "translate-x-0" : "-translate-x-full"
        } md:translate-x-0 md:static`}
      >
        {/* Header del sidebar con logo/título */}
        <div className="bg-brand-dark/40 backdrop-blur-sm p-6 border-b border-brand-vibrant/30">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Image 
                src="/img/plazadedatos.jpg" 
                alt="Plaza de Datos Logo" 
                width={48} 
                height={48} 
                className="rounded-xl shadow-lg"
              />
              <div>
                <h2 className="text-xl font-bold">Plaza de Datos</h2>
                <p className="text-xs text-brand-light/80">Panel de Control</p>
              </div>
            </div>
            <button
              onClick={() => setMenuOpen(false)}
              className="md:hidden text-white hover:bg-brand-vibrant p-2 rounded-lg transition-colors"
            >
              <FaTimes className="text-xl" />
            </button>
          </div>
        </div>

        {/* Contenedor scrolleable para el contenido */}
        <div className="flex-1 overflow-y-auto custom-scrollbar">
          {/* Navegación principal */}
          <nav className="p-4 space-y-2">
            <p className="text-xs font-semibold text-brand-light/70 uppercase tracking-wider px-3 mb-3">
              Navegación Principal
            </p>
            
            <Link 
              href="/panel" 
              className="flex items-center gap-3 hover:bg-brand-vibrant/50 p-3 rounded-xl transition-all duration-200 hover:translate-x-1 group"
              onClick={() => setMenuOpen(false)}
            >
              <div className="w-8 h-8 bg-brand-medium rounded-lg flex items-center justify-center group-hover:bg-brand-light transition-colors">
                <FaHome className="text-sm" />
              </div>
              <span className="font-medium">Inicio</span>
            </Link>
            
            <Link 
              href="/panel/encuestas" 
              className="flex items-center gap-3 hover:bg-brand-vibrant/50 p-3 rounded-xl transition-all duration-200 hover:translate-x-1 group"
              onClick={() => setMenuOpen(false)}
            >
              <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center group-hover:bg-purple-500 transition-colors">
                <FaPoll className="text-sm" />
              </div>
              <span className="font-medium">Encuestas</span>
            </Link>
            
            <Link 
              href="/panel/recompensas" 
              className="flex items-center gap-3 hover:bg-brand-vibrant/50 p-3 rounded-xl transition-all duration-200 hover:translate-x-1 group"
              onClick={() => setMenuOpen(false)}
            >
              <div className="w-8 h-8 bg-yellow-600 rounded-lg flex items-center justify-center group-hover:bg-yellow-500 transition-colors">
                <FaGift className="text-sm" />
              </div>
              <span className="font-medium">Recompensas</span>
            </Link>
            
            <Link 
              href="/panel/misdatos" 
              className="flex items-center gap-3 hover:bg-brand-vibrant/50 p-3 rounded-xl transition-all duration-200 hover:translate-x-1 group"
              onClick={() => setMenuOpen(false)}
            >
              <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center group-hover:bg-green-500 transition-colors">
                <FaUser className="text-sm" />
              </div>
              <span className="font-medium">Mis Datos</span>
            </Link>
            
            <Link 
              href="/panel/historial" 
              className="flex items-center gap-3 hover:bg-brand-vibrant/50 p-3 rounded-xl transition-all duration-200 hover:translate-x-1 group"
              onClick={() => setMenuOpen(false)}
            >
              <div className="w-8 h-8 bg-orange-600 rounded-lg flex items-center justify-center group-hover:bg-orange-500 transition-colors">
                <FaHistory className="text-sm" />
              </div>
              <span className="font-medium">Historial</span>
            </Link>
          </nav>

          {/* Sección Administración */}
          {(user?.rol_id === 1) && (
            <div className="p-4 border-t border-brand-vibrant/30">
              <p className="text-xs font-semibold text-brand-light/70 uppercase tracking-wider px-3 mb-3">
                Administración
              </p>
              
              <button
                onClick={() => setAdminOpen(!adminOpen)}
                className="w-full flex items-center justify-between hover:bg-brand-vibrant/50 p-3 rounded-xl transition-all duration-200 group"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-red-600 rounded-lg flex items-center justify-center group-hover:bg-red-500 transition-colors">
                    <FaTools className="text-sm" />
                  </div>
                  <span className="font-medium">Panel Admin</span>
                </div>
                <FaChevronDown className={`text-brand-light/70 transition-transform duration-200 ${adminOpen ? 'rotate-180' : ''}`} />
              </button>
              
              {adminOpen && (
                <div className="mt-2 ml-4 space-y-1 animate-fade-in-slide">
                  <Link 
                    href="/administracion/dashboard" 
                    className="flex items-center gap-3 hover:bg-brand-vibrant/30 p-2 pl-4 rounded-lg transition-all duration-200 hover:translate-x-1"
                    onClick={() => setMenuOpen(false)}
                  >
                    <FaChartBar className="text-brand-light/70" />
                    <span className="text-sm">Dashboard</span>
                  </Link>
                  <Link 
                    href="/administracion/encuestas" 
                    className="flex items-center gap-3 hover:bg-brand-vibrant/30 p-2 pl-4 rounded-lg transition-all duration-200 hover:translate-x-1"
                    onClick={() => setMenuOpen(false)}
                  >
                    <FaPoll className="text-brand-light/70" />
                    <span className="text-sm">Gestión Encuestas</span>
                  </Link>
                  <Link 
                    href="/administracion/recompensas" 
                    className="flex items-center gap-3 hover:bg-brand-vibrant/30 p-2 pl-4 rounded-lg transition-all duration-200 hover:translate-x-1"
                    onClick={() => setMenuOpen(false)}
                  >
                    <FaGift className="text-brand-light/70" />
                    <span className="text-sm">Gestión Premios</span>
                  </Link>
                  <Link 
                    href="/administracion/configuracion-inicial" 
                    className="flex items-center gap-3 hover:bg-brand-vibrant/30 p-2 pl-4 rounded-lg transition-all duration-200 hover:translate-x-1"
                    onClick={() => setMenuOpen(false)}
                  >
                    <FaCog className="text-brand-light/70" />
                    <span className="text-sm">Config. Inicial</span>
                  </Link>
                  <Link 
                    href="/administracion/resultados-agregados" 
                    className="flex items-center gap-3 hover:bg-brand-vibrant/30 p-2 pl-4 rounded-lg transition-all duration-200 hover:translate-x-1"
                    onClick={() => setMenuOpen(false)}
                  >
                    <FaChartBar className="text-brand-light/70" />
                    <span className="text-sm">Resultados Encuestas</span>
                  </Link>
                  <Link 
                    href="/administracion/respuestas-detalladas" 
                    className="flex items-center gap-3 hover:bg-brand-vibrant/30 p-2 pl-4 rounded-lg transition-all duration-200 hover:translate-x-1"
                    onClick={() => setMenuOpen(false)}
                  >
                    <FaHistory className="text-brand-light/70" />
                    <span className="text-sm">Respuestas Detalladas</span>
                  </Link>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer del sidebar - Usuario y cierre de sesión */}
        <div className="bg-brand-dark/40 backdrop-blur-sm p-4 border-t border-brand-vibrant/30">
          {/* Tarjeta de usuario mejorada */}
          <div className="bg-gradient-to-r from-brand-vibrant/50 to-brand-medium/50 rounded-xl p-4 mb-3 backdrop-blur-sm">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-12 h-12 bg-gradient-to-br from-brand-light to-brand-medium rounded-full flex items-center justify-center text-white font-bold text-lg shadow-lg">
                {user?.nombre?.[0]}{user?.apellido?.[0]}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-white truncate">
                  {user?.nombre} {user?.apellido}
                </p>
                <p className="text-xs text-brand-light/70 truncate">
                  {user?.email}
                </p>
              </div>
            </div>
            
            {/* Indicador de puntos mejorado */}
            <div className="bg-brand-dark/50 rounded-lg p-2 flex items-center justify-between">
              <span className="text-xs text-brand-light/70">Puntos disponibles</span>
              <span className="text-lg font-bold text-yellow-400">
                {user?.puntos_disponibles || 0}
              </span>
            </div>
          </div>
          
          {/* Botón de cierre de sesión mejorado */}
          <button
            onClick={logout}
            className="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white py-3 px-4 rounded-xl transition-all duration-200 flex items-center justify-center gap-2 font-medium shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
          >
            <FaSignOutAlt />
            <span>Cerrar sesión</span>
          </button>
        </div>
      </aside>


    </>
  );
}
