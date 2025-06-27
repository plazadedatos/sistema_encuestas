"use client";

import TopbarInterno from "../../components/TopbarInterno";
import Sidebar from "../../components/Sidebar";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../context/authContext";

export default function PanelPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) router.push("/login");
  }, [isAuthenticated, router]);

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-1">
        <TopbarInterno />
        <main className="p-6">
          <h2 className="text-2xl font-bold mb-4">Bienvenido al Panel</h2>
          <p className="text-gray-600">Aquí podrás gestionar las encuestas y ver tus recompensas.</p>
        </main>
      </div>
    </div>
  );
}
