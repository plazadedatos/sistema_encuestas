"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/authContext";
import { useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/app/services/api";

interface ParticipacionItem {
  id_participacion: number;
  id_encuesta: number;
  titulo_encuesta: string;
  fecha_participacion: string;
  puntaje_obtenido: number;
  tiempo_respuesta_segundos: number;
}

export default function HistorialPage() {
  const { user, isAuthenticated, loading } = useAuth();
  const [historial, setHistorial] = useState<ParticipacionItem[]>([]);
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push("/login");
    }
  }, [loading, isAuthenticated]);

  useEffect(() => {
    const fetchHistorial = async () => {
      if (!user) return;
      try {
        const res = await api.get(
          `/respuestas/participaciones/${(user as any).id || user.id}`
        );
        setHistorial(res.data);
      } catch (error) {
        console.error("Error cargando historial", error);
      }
    };

    fetchHistorial();
  }, [user]);

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-blue-800 mb-6">Mi Historial</h1>

      {historial.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">Aún no has respondido ninguna encuesta.</p>
          <Link 
            href="/panel/encuestas"
            className="mt-4 inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Ver encuestas disponibles
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {historial.map((item) => (
            <div
              key={item.id_participacion}
              className="bg-white shadow-md rounded-xl p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h2 className="text-lg font-semibold text-blue-700 mb-2">
                    {item.titulo_encuesta}
                  </h2>
                  <div className="space-y-1 text-sm text-gray-600">
                    <p>📅 Respondida el {new Date(item.fecha_participacion).toLocaleDateString()}</p>
                    <p>⭐ Puntaje obtenido: <span className="font-semibold text-green-600">{item.puntaje_obtenido} puntos</span></p>
                    <p>⏱️ Tiempo de respuesta: {Math.round(item.tiempo_respuesta_segundos / 60)} minutos</p>
                  </div>
                </div>
                <Link
                  href={`/panel/historial/${item.id_participacion}`}
                  className="ml-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm"
                >
                  Ver detalle →
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
