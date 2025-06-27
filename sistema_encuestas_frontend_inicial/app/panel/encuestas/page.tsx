
"use client";
import TopbarInterno from "../../../components/TopbarInterno";
import Sidebar from "../../../components/Sidebar";
export default function EncuestasPage() {
  return (
    
    <div className="flex min-h-screen bg-slate-50">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          <TopbarInterno />
            <h1 className="text-2xl font-bold text-primary mb-4">Encuestas Disponibles</h1>
            <p className="text-gray-700">Aquí aparecerán las encuestas activas para responder.</p>
        </div>
    </div>
  );
}
