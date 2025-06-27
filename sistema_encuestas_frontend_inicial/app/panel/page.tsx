"use client";

import TopbarInterno from "../../components/TopbarInterno";
import Sidebar from "../../components/Sidebar";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../context/authContext";
import { FaBullhorn, FaGift } from "react-icons/fa";

export default function PanelPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const { user } = useAuth();

  useEffect(() => {
    if (!isAuthenticated) router.push("/");
  }, [isAuthenticated, router]);

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <TopbarInterno />
        <main className="p-8 flex-1">
    <div className="p-6">
        <h1 className="text-3xl font-bold text-blue-800 mb-4">
        ¡Hola, {user?.nombre} {user?.apellido}!
        </h1>

      <p className="text-gray-700">
        Comparte tu opinión en las encuestas y canjea tus puntos por recompensas.
      </p>
    </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Tarjeta: Encuestas */}
            <div className="bg-violet-200/80 rounded-3xl p-8 shadow-xl hover:scale-105 transition duration-300">
              <div className="flex items-center gap-4 mb-4">
                <div className="bg-violet-400 text-white p-4 rounded-full">
                  <FaBullhorn className="text-2xl" />
                </div>
                <h3 className="text-xl font-semibold text-violet-800">¡COMPARTE TU OPINIÓN!</h3>
              </div>
              <p className="text-sm text-violet-900">
                Revisa las encuestas disponibles, responde y suma puntos a tu cuenta.
              </p>
            </div>

            {/* Tarjeta: Recompensas */}
            <div className="bg-sky-200/80 rounded-3xl p-8 shadow-xl hover:scale-105 transition duration-300">
              <div className="flex items-center gap-4 mb-4">
                <div className="bg-sky-400 text-white p-4 rounded-full">
                  <FaGift className="text-2xl" />
                </div>
                <h3 className="text-xl font-semibold text-sky-800">¡CANJEA TUS PUNTOS!</h3>
              </div>
              <p className="text-sm text-sky-900">
                Acumula puntos y canjea por los premios que tenemos para ti.
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
