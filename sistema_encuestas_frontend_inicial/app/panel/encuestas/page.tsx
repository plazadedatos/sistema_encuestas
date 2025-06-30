
// app/panel/encuestas/page.tsx
"use client"


import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import TopbarInterno from "../../../components/TopbarInterno";
import Sidebar from "../../../components/Sidebar";


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
      const response = await api.get("/api/encuestas/activas");
      setEncuestas(response.data);
    } catch (error) {
      console.error("Error al obtener encuestas:", error);
    }
  };

  fetchEncuestas();
}, []);


return (
  <div className="flex">
    <Sidebar />

    <div className="flex-1 flex flex-col min-h-screen bg-gradient-to-br from-white via-blue-50 to-white">
      <TopbarInterno />

      <main className="p-6">
        <h1 className="text-4xl font-bold text-center text-blue-800 mb-10">
          Encuestas Disponibles
        </h1>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {encuestas.map((encuesta) => (
            <Card
              key={encuesta.id_encuesta}
              className="rounded-2xl shadow-md hover:shadow-lg transition duration-300 bg-white flex flex-col justify-between h-[400px]"
            >
            <Image
              src={encuesta.imagen || "/img/default.jpg"}
              alt="imagen encuesta"
              width={400}
              height={200}
              className="rounded-t-2xl w-full h-[200px] object-cover"
            />



              <CardContent className="p-5 space-y-3">
                <h2 className="text-xl font-semibold text-blue-700">
                  {encuesta.titulo}
                </h2>
                <p className="text-gray-600 text-sm leading-tight">
                  {encuesta.descripcion}
                </p>
                <div className="text-sm text-gray-500">
                  <p>
                    <strong>Disponible:</strong> {encuesta.fecha_inicio} al {encuesta.fecha_fin}
                  </p>
                  <p>
                    <strong>Puntos:</strong> {encuesta.puntos_otorga}
                  </p>
                  <p>
                    <strong>Tiempo estimado:</strong> {encuesta.tiempo_estimado}
                  </p>
                </div>
                <Link href={`/panel/encuestas/${encuesta.id_encuesta}`} className="block">
                  <Button className="w-full bg-blue-600 hover:bg-blue-700 transition text-white">
                    Responder Encuesta
                  </Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>
    </div>
  </div>
);

}
