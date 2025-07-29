'use client';

import { useAuth } from '@/context/authContext';
import { useState, useRef, useEffect } from 'react';

export default function Topbar() {
  const { user, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  const nombre = `${user?.nombre ?? ''} ${user?.apellido ?? ''}`.trim();
  const inicial = user?.nombre?.[0]?.toUpperCase() ?? 'U';

  // ✅ Cerrar el menú si se hace clic fuera
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <header className="w-full bg-white shadow flex justify-end items-center px-6 py-3 border-b z-10 sticky top-0">
      <div className="flex items-center gap-3" ref={menuRef}>
        {/* Nombre del usuario */}
        <span className="text-gray-800 font-medium hidden sm:inline">
          {nombre}
        </span>

        {/* Avatar */}
        <button
          onClick={() => setMenuOpen(prev => !prev)}
          className="w-10 h-10 bg-blue-600 text-white flex items-center justify-center rounded-full text-lg font-semibold focus:outline-none"
        >
          {inicial}
        </button>

        {/* Menú desplegable */}
        {menuOpen && (
          <div className="absolute right-6 top-16 w-40 bg-white rounded shadow-md border z-50">
            <ul className="py-1 text-sm text-gray-700">
              <li>
                <button
                  className="w-full text-left px-4 py-2 hover:bg-gray-100"
                  onClick={() => {
                    setMenuOpen(false);
                    alert('Redirigir a perfil próximamente...');
                  }}
                >
                  Mi perfil
                </button>
              </li>
              <li>
                <button
                  className="w-full text-left px-4 py-2 hover:bg-red-100 text-red-600"
                  onClick={logout}
                >
                  Cerrar sesión
                </button>
              </li>
            </ul>
          </div>
        )}
      </div>
    </header>
  );
}
