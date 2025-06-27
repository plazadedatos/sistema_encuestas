"use client";

import Sidebar from "@/components/Sidebar";
import TopbarInterno from "@/components/TopbarInterno";

export default function AdministrarEncuestasPage() {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 flex flex-col min-h-screen">
        <TopbarInterno />

        <main className="p-6">
          <h1 className="text-2xl font-bold text-blue-800 mb-4">Administrar Encuestas</h1>

          {/* Área para crear encuestas */}
          <div className="bg-white shadow rounded-lg p-6">
            <p className="text-gray-700">
              Aquí podrás crear nuevas encuestas, editar preguntas y administrar respuestas.
            </p>

            {/* Próximamente: formulario para nueva encuesta */}
          </div>
        </main>
      </div>
    </div>
  );
}
