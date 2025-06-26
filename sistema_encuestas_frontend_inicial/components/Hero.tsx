"use client";

import { FaGift, FaClock, FaTrophy } from "react-icons/fa";
import { useEffect, useState, useRef } from "react";

import { Link as ScrollLink } from "react-scroll";
import Image from "next/image";
const fotos = ["/img/encuesta1.webp", "/img/encuesta2.webp", "/img/encuesta3.webp"];


export default function Hero() {
    const heroRef = useRef<HTMLDivElement>(null); // 👈 crea la referencia

  const [i, setI] = useState(0);
 useEffect(() => {
  let id: number, t0 = performance.now();
  function ciclo(t: number) {
    if (t - t0 > 5000) {
      setI((v) => (v + 1) % fotos.length);
      t0 = t;
    }
    id = requestAnimationFrame(ciclo);
  }

  const el = heroRef.current;
  if (!el) return;

  const obs = new IntersectionObserver(
    ([e]) => {
      if (!e.isIntersecting) {
        cancelAnimationFrame(id);
      } else {
        id = requestAnimationFrame(ciclo);
      }
    },
    { rootMargin: "0px" }
  );

  obs.observe(el);

  return () => {
    cancelAnimationFrame(id);
    obs.disconnect();
  };
}, []);


  useEffect(() => {
  const actualizar = () => {
    document.documentElement.style.setProperty(
      "--scrollY",
      window.scrollY.toString()
    );
  };
  window.addEventListener("scroll", actualizar, { passive: true });
  return () => window.removeEventListener("scroll", actualizar);
}, []);


  return (
    <section  
    id="hero"
    ref={heroRef}  
    className="mx-auto my-10 max-w-7xl rounded-3xl overflow-hidden shadow-2xl shadow-black/20 animate-fade">
      {/* fondo cambiante */}
      {fotos.map((f, idx) => (
      <Image
        key={`${f}-${idx}`} // <-- 🔧 Aquí está la corrección
        fill
        src={f}
        alt=""
        priority={idx === i}
        quality={80}
        className={`absolute inset-0 object-cover transition-opacity duration-700
            ${idx === i ? "opacity-100 z-0" : "opacity-0"}`}
      />
    ))}



      {/* gradiente overlay + blur */}
      <div className="absolute inset-0 bg-primary/75" />

      {/* grid */}
      <div className="relative z-10 grid md:grid-cols-2 gap-10 p-10 md:p-20 text-white">
{/* IZQ – Formulario de Registro */}
<div className="flex flex-col justify-center">
  <div className="bg-white/90 p-8 rounded-2xl shadow-lg w-full max-w-md mx-auto text-primary">
    <h3 className="text-xl font-bold text-center mb-6">Crea tu Cuenta</h3>

    <form className="space-y-4 text-sm">
      <input type="text" placeholder="Nombre"
        className="w-full px-4 py-2 rounded-full border focus:outline-none focus:ring-2 focus:ring-primary-light transition"
      />
      <input type="text" placeholder="Apellido"
        className="w-full px-4 py-2 rounded-full border focus:outline-none focus:ring-2 focus:ring-primary-light transition"
      />
      <input type="text" placeholder="N° Cédula"
        className="w-full px-4 py-2 rounded-full border focus:outline-none focus:ring-2 focus:ring-primary-light transition"
      />
      <input type="email" placeholder="Correo Electrónico"
        className="w-full px-4 py-2 rounded-full border focus:outline-none focus:ring-2 focus:ring-primary-light transition"
      />
      <input type="password" placeholder="Contraseña"
        className="w-full px-4 py-2 rounded-full border focus:outline-none focus:ring-2 focus:ring-primary-light transition"
      />
      <input type="password" placeholder="Repetir Contraseña"
        className="w-full px-4 py-2 rounded-full border focus:outline-none focus:ring-2 focus:ring-primary-light transition"
      />

      <button
        type="submit"
        className="w-full bg-primary text-white py-2 rounded-full font-semibold hover:bg-primary-dark transition"
      >
        Regístrate
      </button>
    </form>
    
  </div>
   <h1 className="text-xl font-bold text-center mb-6"> Tu opinion Tiene Recompensas en Plaza de Datos</h1>
</div>


        {/* DER */}
        <div className="flex flex-col justify-center items-start md:items-end text-right">
          <h1 className="text-4xl md:text-5xl font-extrabold mb-4">
            ¡Tu Opinión Nos Importa!
          </h1>
          <p className="text-lg md:text-xl mb-6 opacity-90">
            Participa en Nuestras Encuestas y gana puntos para canjearlos.
          </p>

          <ul className="space-y-2 text-md mb-8">
            <li className="flex items-center gap-2 justify-end">
              <FaTrophy className="text-yellow-300" /> Recompensas Exclusivas
            </li>
            <li className="flex items-center gap-2 justify-end">
              <FaClock className="text-emerald-300" /> Solo minutos
            </li>
            <li className="flex items-center gap-2 justify-end">
              <FaGift className="text-pink-300" /> Premios Reales
            </li>
          </ul>

          <ScrollLink to="encuestas" smooth duration={100} offset={-80}>
            <button className="px-8 py-3 rounded-full bg-gradient-to-r from-white/90 to-white text-primary font-bold shadow hover:scale-105 transition">
              Comenzar Ahora
            </button>
          </ScrollLink>
        </div>
      </div>
    </section>
  );
}
