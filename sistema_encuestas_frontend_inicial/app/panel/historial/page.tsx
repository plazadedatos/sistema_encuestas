"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/authContext";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import TopbarInterno from "@/components/TopbarInterno";

import api from "@/app/services/api";
interface HistorialItem {
  id_encuesta: number;
  titulo: string;
  fecha_respuesta: string;
  cantidad_respuestas: number;
}

export default function HistorialPage() {
  const { user, isAuthenticated, loading } = useAuth();
  const [historial, setHistorial] = useState<HistorialItem[]>([]);
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
        const res = await api.get(`/api/respuestas/historial/${user.usuario_id}`);
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
                  key={item.id_encuesta}
                  className="bg-white shadow rounded-xl p-4 flex justify-between items-center"
                >
                  <div>
                    <h2 className="text-lg font-semibold text-blue-700">{item.titulo}</h2>
                    <p className="text-sm text-gray-600">
                      Respondida el {new Date(item.fecha_respuesta).toLocaleDateString()}
                    </p>
                    <p className="text-sm text-gray-500">{item.cantidad_respuestas} respuestas</p>
                  </div>
                  <button
                    onClick={() => alert("Funcionalidad de detalle próximamente")}
                    className="text-blue-600 hover:underline text-sm"
                  >
                    Ver detalle →
                  </button>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
