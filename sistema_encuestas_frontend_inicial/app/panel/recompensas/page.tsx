"use client";
import TopbarInterno from "../../../components/TopbarInterno";
import Sidebar from "../../../components/Sidebar";
export default function RecompensasPage() {
  return (
    
    <div className="flex min-h-screen bg-slate-50">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          <TopbarInterno />
          <h1 className="text-2xl font-bold text-pink-600 mb-4">Tus Recompensas</h1>
          <p className="text-gray-700">Acumula puntos y canjéalos por productos o premios.</p>
      </div>
    </div>
  );
}
