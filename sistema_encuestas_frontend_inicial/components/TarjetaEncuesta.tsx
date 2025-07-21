import { FaCalendar, FaClock, FaTrophy } from "react-icons/fa";
import Image from "next/image";

interface Encuesta {
  id_encuesta: number;
  titulo: string;
  descripcion: string;
  fecha_inicio: string;
  fecha_fin: string;
  puntos_otorga: number;
  imagen?: string | null;
  tiempo_estimado?: string;
  preguntas?: any[]; // Agregar propiedad opcional
}

interface TarjetaEncuestaProps {
  encuesta: Encuesta;
  mostrarEstado?: boolean;
  onParticipate?: () => void;
}

export default function TarjetaEncuesta({
  encuesta,
  mostrarEstado = false,
  onParticipate
}: TarjetaEncuestaProps) {
  return (
    <article className="group bg-white rounded-2xl shadow-lg overflow-hidden transition-all duration-300 hover:-translate-y-1 hover:shadow-xl flex flex-col h-full">
      {/* Imagen de la encuesta */}
      <div className="relative h-48 sm:h-56 lg:h-48 bg-gray-100">
        <Image
          src={encuesta.imagen || "/img/default.jpg"}
          alt={`Imagen de ${encuesta.titulo}`}
          fill
          className="object-cover"
          sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      </div>

      {/* Contenido */}
      <div className="p-5 flex flex-col flex-1">
        <h3 className="text-lg sm:text-xl font-bold text-gray-800 mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors">
          {encuesta.titulo}
        </h3>
        
        <p className="text-sm text-gray-600 mb-4 line-clamp-3 flex-1">
          {encuesta.descripcion}
        </p>

        {/* Información adicional */}
        <div className="space-y-2 text-xs sm:text-sm text-gray-500 mb-4">
          <div className="flex items-center gap-2">
            <FaCalendar className="text-blue-500" />
            <span className="truncate">
              Hasta: {new Date(encuesta.fecha_fin).toLocaleDateString('es-ES', {
                day: 'numeric',
                month: 'short',
                year: 'numeric'
              })}
            </span>
          </div>
          
          <div className="flex items-center gap-2">
            <FaTrophy className="text-yellow-500" />
            <span className="font-semibold text-green-600">
              {encuesta.puntos_otorga} puntos
            </span>
          </div>
          
          {encuesta.tiempo_estimado && (
            <div className="flex items-center gap-2">
              <FaClock className="text-purple-500" />
              <span>{encuesta.tiempo_estimado}</span>
            </div>
          )}
        </div>

        {/* Botón de acción */}
        <button
          onClick={onParticipate}
          className="w-full py-2.5 px-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white font-medium rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Responder Encuesta
        </button>
      </div>
    </article>
  );
}
