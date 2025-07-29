'use client';
import { FaFacebook, FaInstagram, FaTwitter } from 'react-icons/fa';
import { HiOutlineMail } from 'react-icons/hi';
import { GoLocation } from 'react-icons/go';

export default function Footer() {
  return (
    <footer className="bg-gradient-to-t from-primary-dark via-primary to-primary-light text-white mt-20 shadow-inner pt-10">
      <div className="max-w-7xl mx-auto px-6 grid md:grid-cols-3 gap-10 pb-12">
        {/* SOBRE */}
        <div>
          <h3 className="font-semibold text-lg mb-2">Sobre Nosotros</h3>
          <p className="text-sm leading-relaxed opacity-90">
            Plataforma de encuestas inteligentes con recompensas reales.
            Participa, gana puntos y canjea premios por tu opinión.
          </p>
        </div>

        {/* CONTACTO */}
        <div>
          <h3 className="font-semibold text-lg mb-2">Contacto</h3>
          <ul className="text-sm space-y-1 opacity-90">
            <li className="flex items-center gap-2">
              <HiOutlineMail className="text-lg" />
              contacto@encuestas.com
            </li>
            <li className="flex items-center gap-2">
              <GoLocation className="text-lg" />
              San Lorenzo – Paraguay
            </li>
          </ul>
        </div>

        {/* REDES */}
        <div>
          <h3 className="font-semibold text-lg mb-2">Síguenos</h3>
          <div className="flex gap-4 text-xl mt-2">
            <a
              href="#"
              className="hover:text-yellow-300 hover:scale-110 transition duration-300"
            >
              <FaFacebook />
            </a>
            <a
              href="#"
              className="hover:text-yellow-300 hover:scale-110 transition duration-300"
            >
              <FaInstagram />
            </a>
            <a
              href="#"
              className="hover:text-yellow-300 hover:scale-110 transition duration-300"
            >
              <FaTwitter />
            </a>
          </div>
        </div>
      </div>

      {/* COPYRIGHT */}
      <div className="text-center text-sm bg-primary-dark/80 py-3">
        © {new Date().getFullYear()} Plaza de Datos. Todos los derechos
        reservados.
      </div>
    </footer>
  );
}
