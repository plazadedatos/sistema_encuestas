"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

import { Link as ScrollLink } from "react-scroll";   // 👈 IMPORTA AQUÍ
export default function Topbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const manejarScroll = () => {
      setScrolled(window.scrollY > 10); // si bajó 10px o más, se activa
    };

    window.addEventListener("scroll", manejarScroll);
    return () => window.removeEventListener("scroll", manejarScroll);
  }, []);

  return (
    <header
      className={`
        fixed top-0 left-0 right-0 z-50
        transition-all duration-300
        ${scrolled ? "bg-white/80 backdrop-blur-md shadow-md" : "bg-primary text-white"}
      `}
    >
      <nav className="max-w-7xl mx-auto flex justify-between items-center h-16 px-4">
        <div className="flex gap-6 items-center font-semibold">
          <Link href="/" className="text-xl font-bold">
            Plaza de Datos<span className={scrolled ? "text-primary" : "text-white"}></span>
          </Link>
          <ul className="hidden md:flex gap-4 text-sm">
            <li><ScrollLink to="hero" smooth duration={100} offset={-80} className="cursor-pointer">Inicio</ScrollLink></li>
            <li><ScrollLink to="encuestas" smooth duration={100} offset={-80} className="cursor-pointer">Encuestas</ScrollLink></li>
            <li><ScrollLink to="faq" smooth duration={100} offset={-80} className="cursor-pointer">Preguntas frecuentes</ScrollLink></li> {/* ← NUEVO */}
            <li><ScrollLink to="nosotros" smooth duration={100} offset={-80} className="cursor-pointer">Nosotros</ScrollLink></li>
            <li><Link href="/noticias">Noticias</Link></li>
          </ul>
        </div>
        <div className="flex gap-2 text-sm">
          <Link
            href="/login"
            className={`px-3 py-1 rounded border ${
              scrolled
                ? "border-primary text-primary hover:bg-primary hover:text-white"
                : "border-white text-white hover:bg-white hover:text-primary"
            } transition`}
          >
            Iniciar sesión
          </Link>
          <Link
            href="/registro"
            className={`px-3 py-1 rounded bg-white text-primary font-semibold hover:bg-primary-light hover:text-white transition ${
              scrolled ? "border border-primary" : ""
            }`}
          >
            Registrarse
          </Link>
        </div>
      </nav>
    </header>
  );
}
