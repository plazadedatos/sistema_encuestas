// app/panel/encuestas/[id]/page.tsx
"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import TopbarInterno from "@/components/TopbarInterno";
import { useAuth } from "../../../../context/authContext";

interface Opcion {
  id_opcion: number;
  texto_opcion: string;
}

interface Pregunta {
  id_pregunta: number;
  texto: string;
  tipo: string;
  orden: number;
  opciones: Opcion[];
}

interface Encuesta {
  id_encuesta: number;
  titulo: string;
  descripcion: string;
  preguntas: Pregunta[];
}

export default function ResponderEncuestaPage() {
  const { id } = useParams();
  const [encuesta, setEncuesta] = useState<Encuesta | null>(null);
  const [respuestas, setRespuestas] = useState<any>({});
  const [cargando, setCargando] = useState(true);
    const { isAuthenticated, user } = useAuth();
  useEffect(() => {
    const obtenerEncuesta = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/api/encuestas/${id}`);
        setEncuesta(res.data);
      } catch (error) {
        console.error("Error cargando encuesta", error);
      } finally {
        setCargando(false);
      }
    };

    obtenerEncuesta();
  }, [id]);

  const manejarCambio = (id_pregunta: number, valor: any) => {
    setRespuestas((prev: any) => ({ ...prev, [id_pregunta]: valor }));
  };

  const enviarRespuestas = async () => {
    try {
      const payload = Object.entries(respuestas).map(([id_pregunta, valor]) => ({
        id_pregunta: Number(id_pregunta),
        id_usuario: 1, // ⚠️ reemplazar luego por usuario autenticado
        id_opcion: typeof valor === "number" ? valor : null,
        respuesta_texto: typeof valor === "string" ? valor : null,
        fecha_respuesta: new Date().toISOString(),
      }));

      await axios.post("http://localhost:8000/api/respuestas/", {
        id_usuario: user?.sub,
        respuestas: payload
        });

      alert("Respuestas enviadas exitosamente ✅");
    } catch (err) {
      console.error("Error al enviar respuestas", err);
      alert("Ocurrió un error al enviar respuestas ❌");
    }
  };

  if (cargando) return <p className="p-10">Cargando encuesta...</p>;
  if (!encuesta) return <p className="p-10 text-red-500">Encuesta no encontrada</p>;

  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1">
        <TopbarInterno />

        <main className="max-w-3xl mx-auto py-10 px-4">
          <h1 className="text-3xl font-bold text-blue-800 mb-6">{encuesta.titulo}</h1>
          <p className="text-gray-600 mb-10">{encuesta.descripcion}</p>

          <form className="space-y-8">
            {encuesta.preguntas.map((p) => (
              <div key={p.id_pregunta} className="bg-white p-4 rounded-xl shadow">
                <p className="font-medium mb-2">{p.texto}</p>

                {p.tipo === "texto_libre" ? (
                  <textarea
                    className="w-full border rounded p-2"
                    value={respuestas[p.id_pregunta] || ""}
                    onChange={(e) => manejarCambio(p.id_pregunta, e.target.value)}
                  />
                ) : (
                  <div className="space-y-2">
                    {p.opciones.map((op) => (
                      <label key={op.id_opcion} className="block">
                        <input
                          type="radio"
                          name={`pregunta_${p.id_pregunta}`}
                          value={op.id_opcion}
                          checked={respuestas[p.id_pregunta] === op.id_opcion}
                          onChange={() => manejarCambio(p.id_pregunta, op.id_opcion)}
                          className="mr-2"
                        />
                        {op.texto_opcion}
                      </label>
                    ))}
                  </div>
                )}
              </div>
            ))}

            <button
              type="button"
              onClick={enviarRespuestas}
              className="w-full mt-6 bg-blue-700 text-white py-3 rounded-lg hover:bg-blue-800"
            >
              Enviar Respuestas
            </button>
          </form>
        </main>
      </div>
    </div>
  );
}