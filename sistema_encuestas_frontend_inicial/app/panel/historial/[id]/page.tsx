"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import TopbarInterno from "@/components/TopbarInterno";
import api from "@/app/services/api";
import Link from "next/link";

interface PreguntaDetalle {
  id_pregunta: number;
  texto: string;
  tipo: string;
  respuesta_texto: string | null;
  opcion_elegida: string | null;
  fecha_respuesta: string;
}

interface ParticipacionDetalle {
  id_participacion: number;
  encuesta: {
    id_encuesta: number;
    titulo: string;
    descripcion: string;
  };
  usuario: number;
  fecha_participacion: string;
  puntaje_obtenido: number;
  tiempo_respuesta_segundos: number;
  preguntas: PreguntaDetalle[];
}

export default function DetalleParticipacionPage() {
  const { id } = useParams();
  const router = useRouter();
  const [detalle, setDetalle] = useState<ParticipacionDetalle | null>(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    const fetchDetalle = async () => {
      try {
        const res = await api.get(`/participaciones/${id}/detalle`);
        setDetalle(res.data);
      } catch (error) {
        console.error("Error cargando detalle", error);
      } finally {
        setCargando(false);
      }
    };

    fetchDetalle();
  }, [id]);

  if (cargando) return <p className="p-10">Cargando detalle...</p>;
  if (!detalle) return <p className="p-10 text-red-500">Detalle no encontrado</p>;

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1">
        <TopbarInterno />

        <main className="max-w-4xl mx-auto py-10 px-4 space-y-6">
          <Link href="/panel/historial" className="text-blue-600 hover:underline">
            ← Volver al historial
          </Link>
          <h1 className="text-3xl font-bold text-blue-800">
            {detalle.encuesta.titulo}
          </h1>
          <p className="text-gray-600">{detalle.encuesta.descripcion}</p>
          <div className="text-sm text-gray-700 space-y-1">
            <p>
              <strong>Fecha:</strong>{" "}
              {new Date(detalle.fecha_participacion).toLocaleString()}
            </p>
            <p>
              <strong>Puntaje obtenido:</strong> {detalle.puntaje_obtenido}
            </p>
            <p>
              <strong>Tiempo de respuesta:</strong> {" "}
              {detalle.tiempo_respuesta_segundos} segundos
            </p>
          </div>

          <section className="space-y-4">
            {detalle.preguntas.map((p) => (
              <div
                key={p.id_pregunta}
                className="bg-white p-4 rounded-xl shadow"
              >
                <p className="font-medium mb-2">{p.texto}</p>
                {p.tipo === "texto_libre" ? (
                  <p className="text-gray-700">Respuesta: {p.respuesta_texto}</p>
                ) : (
                  <p className="text-gray-700">Opción elegida: {p.opcion_elegida}</p>
                )}
              </div>
            ))}
          </section>
        </main>
      </div>
    </div>
  );
}
