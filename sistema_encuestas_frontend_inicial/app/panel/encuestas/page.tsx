// app/panel/encuestas/page.tsx
"use client"

import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import Image from "next/image";
import api from "@/app/services/api";

interface Encuesta {
  id_encuesta: number;
  titulo: string;
  descripcion: string;
  fecha_inicio: string;
  fecha_fin: string;
  puntos_otorga: number;
  imagen: string | null;
  tiempo_estimado: string;
}

export default function EncuestasPage() {
  const [encuestas, setEncuestas] = useState<Encuesta[]>([]);

  useEffect(() => {
    const fetchEncuestas = async () => {
      try {
        const response = await api.get("/encuestas/activas");
        setEncuestas(response.data);
      } catch (error) {
        console.error("Error al obtener encuestas:", error);
      }
    };

    fetchEncuestas();
  }, []);

  return (
    <div className="max-w-7xl mx-auto">
      <h1 className="text-4xl font-bold text-center text-blue-800 mb-10">
        Encuestas Disponibles
      </h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {encuestas.map((encuesta) => (
          <Card
            key={encuesta.id_encuesta}
            className="rounded-2xl shadow-md hover:shadow-lg transition duration-300 bg-white flex flex-col overflow-hidden"
          >
            <div className="relative h-48 sm:h-56 lg:h-48">
              <Image
                src={encuesta.imagen || "/img/default.jpg"}
                alt="imagen encuesta"
                width={400}
                height={200}
                className="absolute inset-0 w-full h-full object-cover"
              />
            </div>

            <CardContent className="p-5 space-y-3 flex-1 flex flex-col">
              <h2 className="text-lg sm:text-xl font-semibold text-blue-700 line-clamp-2">
                {encuesta.titulo}
              </h2>
              <p className="text-gray-600 text-sm leading-relaxed line-clamp-3 flex-1">
                {encuesta.descripcion}
              </p>
              <div className="text-xs sm:text-sm text-gray-500 space-y-1 pt-2 border-t border-gray-100">
                <p className="truncate">
                  <strong>Disponible:</strong> {new Date(encuesta.fecha_inicio).toLocaleDateString()} al {new Date(encuesta.fecha_fin).toLocaleDateString()}
                </p>
                <p>
                  <strong>Puntos:</strong> <span className="text-green-600 font-semibold">{encuesta.puntos_otorga}</span>
                </p>
                <p>
                  <strong>Tiempo estimado:</strong> <span className="text-blue-600">{encuesta.tiempo_estimado}</span>
                </p>
              </div>
              <Link href={`/panel/encuestas/${encuesta.id_encuesta}`} className="block mt-auto pt-3">
                <Button className="w-full bg-blue-600 hover:bg-blue-700 transition text-white py-2.5">
                  Responder Encuesta
                </Button>
              </Link>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
