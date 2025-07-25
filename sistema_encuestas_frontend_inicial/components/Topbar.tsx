"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
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
          <Link href="/" className="flex items-center gap-2 text-xl font-bold">
            <Image 
              src="/img/plazadedatos.jpg" 
              alt="Plaza de Datos Logo" 
              width={40} 
              height={40} 
              className="rounded-lg object-contain"
            />
            <span>Plaza de Datos</span>
          </Link>
          <ul className="hidden md:flex gap-4 text-sm">
            <li><ScrollLink to="hero" smooth duration={100} offset={-80} className="cursor-pointer hover:text-brand-light transition-colors">Inicio</ScrollLink></li>
            <li><ScrollLink to="encuestas" smooth duration={100} offset={-80} className="cursor-pointer hover:text-brand-light transition-colors">Encuestas</ScrollLink></li>
            <li><ScrollLink to="faq" smooth duration={100} offset={-80} className="cursor-pointer hover:text-brand-light transition-colors">Preguntas frecuentes</ScrollLink></li>
            <li><ScrollLink to="nosotros" smooth duration={100} offset={-80} className="cursor-pointer hover:text-brand-light transition-colors">Nosotros</ScrollLink></li>
            <li><Link href="/noticias" className="hover:text-brand-light transition-colors">Noticias</Link></li>
          </ul>
        </div>
        <div className="flex gap-2 text-sm">
          <Link
            href="/login"
            className={`px-3 py-1 rounded border ${
              scrolled
                ? "border-brand-vibrant text-brand-vibrant hover:bg-brand-vibrant hover:text-white"
                : "border-white text-white hover:bg-white hover:text-brand-vibrant"
            } transition-all duration-200`}
          >
            Iniciar sesión
          </Link>
          <Link
            href="/registro"
            className={`px-3 py-1 rounded ${
              scrolled 
                ? "bg-brand-vibrant text-white border border-brand-vibrant hover:bg-brand-dark" 
                : "bg-white text-brand-vibrant hover:bg-brand-light hover:text-white"
            } transition-all duration-200 font-semibold`}
          >
            Registrarse
          </Link>
        </div>
      </nav>
    </header>
  );
}
