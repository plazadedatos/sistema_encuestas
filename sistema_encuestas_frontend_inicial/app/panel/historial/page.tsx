
"use client";
import TopbarInterno from "../../../components/TopbarInterno";
import Sidebar from "../../../components/Sidebar";
export default function HistorialPage() {
  return (
    
    <div className="flex min-h-screen bg-slate-50">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          <TopbarInterno />
            <h1 className="text-2xl font-bold text-indigo-600 mb-4">Historial</h1>
            <p className="text-gray-700">Aquí verás un resumen de tus encuestas respondidas y premios canjeados.</p>
        </div>
    </div>
  );
}
