"use client";

import { useAuth } from "@/context/authContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { FaClipboardList, FaGift, FaHistory, FaUser, FaChartLine, FaTrophy, FaClock, FaLock } from "react-icons/fa";
import Link from "next/link";

export default function PanelPage() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [greeting, setGreeting] = useState("");

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [user, loading, router]);

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) {
      setGreeting("Buenos días");
    } else if (hour < 19) {
      setGreeting("Buenas tardes");
    } else {
      setGreeting("Buenas noches");
    }
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const menuItems = [
    {
      title: "Encuestas Disponibles",
      description: "Responde encuestas y gana puntos",
      icon: <FaClipboardList className="text-3xl" />,
      href: "/panel/encuestas",
      color: "bg-gradient-to-br from-blue-500 to-blue-700",
      iconBg: "bg-blue-100",
      iconColor: "text-blue-600",
      hoverEffect: "hover:from-blue-600 hover:to-blue-800"
    },
    {
      title: "Mis Recompensas",
      description: "Canjea tus puntos por premios",
      icon: <FaGift className="text-3xl" />,
      href: "/panel/recompensas",
      color: "bg-gradient-to-br from-purple-500 to-purple-700",
      iconBg: "bg-purple-100",
      iconColor: "text-purple-600",
      hoverEffect: "hover:from-purple-600 hover:to-purple-800"
    },
    {
      title: "Mi Historial",
      description: "Revisa tus participaciones",
      icon: <FaHistory className="text-3xl" />,
      href: "/panel/historial",
      color: "bg-gradient-to-br from-green-500 to-green-700",
      iconBg: "bg-green-100",
      iconColor: "text-green-600",
      hoverEffect: "hover:from-green-600 hover:to-green-800"
    },
    {
      title: "Mis Datos",
      description: "Gestiona tu perfil",
      icon: <FaUser className="text-3xl" />,
      href: "/panel/misdatos",
      color: "bg-gradient-to-br from-orange-500 to-orange-700",
      iconBg: "bg-orange-100",
      iconColor: "text-orange-600",
      hoverEffect: "hover:from-orange-600 hover:to-orange-800"
    }
  ];

  const statsCards = [
    {
      title: "Puntos Totales",
      value: user?.puntos_totales || 0,
      icon: <FaChartLine />,
      color: "text-blue-600",
      bgColor: "bg-blue-100"
    },
    {
      title: "Puntos Disponibles",
      value: user?.puntos_disponibles || 0,
      icon: <FaTrophy />,
      color: "text-green-600",
      bgColor: "bg-green-100"
    },
    {
      title: "Puntos Canjeados",
      value: user?.puntos_canjeados || 0,
      icon: <FaClock />,
      color: "text-purple-600",
      bgColor: "bg-purple-100"
    }
  ];

  const isAdmin = user?.rol_id === 1 || user?.rol_id === 2;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header con saludo */}
      <div className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-800">
            {greeting}, {user?.nombre}! 👋
          </h1>
          <p className="text-gray-600 mt-2">
            Bienvenido a tu panel de control. ¿Qué deseas hacer hoy?
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Estadísticas */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Tu Resumen</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {statsCards.map((stat, index) => (
              <div
                key={index}
                className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 hover:shadow-md transition-shadow"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">{stat.title}</p>
                    <p className="text-3xl font-bold text-gray-800 mt-2">
                      {stat.value.toLocaleString()}
                    </p>
                  </div>
                  <div className={`${stat.bgColor} p-4 rounded-lg`}>
                    <span className={`${stat.color} text-2xl`}>{stat.icon}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Menu principal */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Acciones Rápidas</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {menuItems.map((item, index) => (
              <Link
                key={index}
                href={item.href}
                className={`group relative overflow-hidden rounded-xl shadow-lg ${item.color} p-6 text-white transform transition-all duration-300 hover:scale-105 ${item.hoverEffect}`}
              >
                <div className="relative z-10">
                  <div className="mb-4">
                    {item.icon}
                  </div>
                  <h3 className="text-xl font-bold mb-2">{item.title}</h3>
                  <p className="text-white/90 text-sm">{item.description}</p>
                </div>
                <div className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 transition-opacity"></div>
              </Link>
            ))}
          </div>
        </div>

        {/* Área de administración */}
        {isAdmin && (
          <div className="mt-12 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-8 border border-indigo-100">
            <div className="flex items-center mb-6">
              <div className="bg-indigo-100 p-3 rounded-lg mr-4">
                <FaLock className="text-2xl text-indigo-600" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-800">Área de Administración</h2>
                <p className="text-gray-600">Accede a las estadísticas y gestión del sistema</p>
              </div>
            </div>
            <Link
              href="/administracion/dashboard"
              className="inline-flex items-center px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors duration-200 shadow-md hover:shadow-lg"
            >
              <FaChartLine className="mr-2" />
              Ir al Dashboard Administrativo
            </Link>
          </div>
        )}

        {/* Mensaje motivacional */}
        <div className="mt-8 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-100">
          <p className="text-center text-gray-700 italic">
            "Tu opinión es valiosa. Cada encuesta que completas nos ayuda a mejorar y te acerca a increíbles recompensas."
          </p>
        </div>
      </div>
    </div>
  );
}
