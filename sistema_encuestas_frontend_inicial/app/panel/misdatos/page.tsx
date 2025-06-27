
"use client";
import TopbarInterno from "../../../components/TopbarInterno";
import Sidebar from "../../../components/Sidebar";
export default function MisDatosPage() {
  return (
    
    <div className="flex min-h-screen bg-slate-50">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          <TopbarInterno />
            <h1 className="text-2xl font-bold text-blue-700 mb-4">Mis Datos</h1>
            <p className="text-gray-700">Revisa y edita la información de tu cuenta.</p>
        </div>
    </div>
  );
}
