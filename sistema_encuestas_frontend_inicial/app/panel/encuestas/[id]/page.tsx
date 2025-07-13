// app/panel/encuestas/[id]/page.tsx
"use client";

import { useEffect, useState } from "react";
import api from "@/app/services/api";
import { useParams, useRouter } from "next/navigation";
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
  const router = useRouter();
  const [encuesta, setEncuesta] = useState<Encuesta | null>(null);
  const [respuestas, setRespuestas] = useState<any>({});
  const [cargando, setCargando] = useState(true);
  const [enviando, setEnviando] = useState(false);
  const { isAuthenticated, user } = useAuth();
  useEffect(() => {
    const obtenerEncuesta = async () => {
      try {
        const res = await api.get(`/encuestas/${id}`);
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
    setEnviando(true);
    try {
      const payload = Object.entries(respuestas).map(([id_pregunta, valor]) => ({
        id_pregunta: Number(id_pregunta),
        id_opcion: typeof valor === "number" ? valor : undefined,
        respuesta_texto: typeof valor === "string" ? valor : undefined,
      }));

      await api.post("/respuestas/", {
        id_encuesta: Number(id),
        respuestas: payload,
      });

      alert("¡Respuestas enviadas exitosamente! ✅ Has ganado puntos por completar esta encuesta.");
      
      // Redirigir al panel principal después de un breve delay
      setTimeout(() => {
        router.push("/panel");
      }, 1500);
      
    } catch (err) {
      console.error("Error al enviar respuestas", err);
      alert("Ocurrió un error al enviar respuestas ❌");
      setEnviando(false);
    }
  };

  if (cargando) return <p className="p-10">Cargando encuesta...</p>;
  if (!encuesta) return <p className="p-10 text-red-500">Encuesta no encontrada</p>;

  return (
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
          disabled={enviando || Object.keys(respuestas).length === 0}
          className={`w-full mt-6 py-3 rounded-lg transition-colors ${
            enviando || Object.keys(respuestas).length === 0
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-700 text-white hover:bg-blue-800"
          }`}
        >
          {enviando ? "Enviando..." : "Enviar Respuestas"}
        </button>
      </form>
    </main>
  );
}
