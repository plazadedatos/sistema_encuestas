"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/authContext";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import TopbarInterno from "@/components/TopbarInterno";
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
          `/api/respuestas/participaciones/${user.usuario_id}`
        );
        setHistorial(res.data);
      } catch (error) {
        console.error("Error cargando historial", error);
      }
    };

    fetchHistorial();
  }, [user]);

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1">
        <TopbarInterno />

        <main className="max-w-4xl mx-auto py-10 px-4">
          <h1 className="text-3xl font-bold text-blue-800 mb-6">Mi Historial</h1>

          {historial.length === 0 ? (
            <p className="text-gray-500">Aún no has respondido ninguna encuesta.</p>
          ) : (
            <div className="space-y-4">
              {historial.map((item) => (
                <div
                  key={item.id_participacion}
                  className="bg-white shadow rounded-xl p-4 flex justify-between items-center"
                >
                  <div>
                    <h2 className="text-lg font-semibold text-blue-700">
                      {item.titulo_encuesta}
                    </h2>
                    <p className="text-sm text-gray-600">
                      Respondida el {new Date(item.fecha_participacion).toLocaleDateString()}
                    </p>
                    <p className="text-sm text-gray-500">
                      Puntaje obtenido: {item.puntaje_obtenido}
                    </p>
                  </div>
                  <Link
                    href={`/panel/historial/${item.id_participacion}`}
                    className="text-blue-600 hover:underline text-sm"
                  >
                    Ver detalle →
                  </Link>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
