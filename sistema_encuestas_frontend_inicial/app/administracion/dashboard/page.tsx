"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/context/authContext";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  BarChart, Bar, PieChart, Pie, LineChart, Line, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts";
import { 
  FaUsers, FaPoll, FaChartLine, FaClock, FaDownload, 
  FaFilter, FaCalendar 
} from "react-icons/fa";
import jsPDF from "jspdf";
import "jspdf-autotable";
import api from "@/app/services/api";
import { toast } from "react-toastify";
import { useAdminAuth } from "../../../hooks/useAdminAuth";

// Tipos de datos
interface DashboardStats {
  totalRespuestas: number;
  usuariosActivos: number;
  encuestasMasRespondidas: Array<{
    titulo: string;
    respuestas: number;
  }>;
  tiempoPromedioRespuesta: number;
}

interface ChartData {
  respuestasPorEncuesta: Array<{
    encuesta: string;
    respuestas: number;
  }>;
  distribucionDemografica: Array<{
    name: string;
    value: number;
  }>;
  respuestasPorDia: Array<{
    fecha: string;
    respuestas: number;
  }>;
}

interface ParticipacionDetalle {
  id: number;
  usuario: string;
  encuesta: string;
  fecha: string;
  duracion: number;
}

// Colores para los gráficos
const COLORS = ['#3B82F6', '#8B5CF6', '#EC4899', '#10B981', '#F59E0B', '#EF4444'];

export default function DashboardPage() {
  const { user, token, loading: authLoading } = useAdminAuth();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [chartData, setChartData] = useState<ChartData | null>(null);
  const [participaciones, setParticipaciones] = useState<ParticipacionDetalle[]>([]);
  const [filtroFecha, setFiltroFecha] = useState("mes");
  const [selectedParticipacion, setSelectedParticipacion] = useState<ParticipacionDetalle | null>(null);

  useEffect(() => {
    if (!authLoading && user && token) {
      console.log("✅ Autenticación verificada, cargando datos del dashboard...");
      cargarDatos();
    }
  }, [authLoading, user, token]);

  const cargarDatos = async () => {
    console.log("📊 Iniciando carga de datos del dashboard...");
    setLoading(true);
    try {
      console.log("🚀 Realizando peticiones paralelas al backend...");
      
      // Cargar datos reales desde el backend
      const [statsRes, chartsRes, participacionesRes] = await Promise.all([
        api.get("/dashboard/stats").catch(err => {
          console.error("❌ Error en /stats:", err);
          throw err;
        }),
        api.get("/dashboard/charts").catch(err => {
          console.error("❌ Error en /charts:", err);
          throw err;
        }),
        api.get("/dashboard/participaciones").catch(err => {
          console.error("❌ Error en /participaciones:", err);
          throw err;
        })
      ]);
      
      console.log("✅ Datos recibidos correctamente");
      setStats(statsRes.data);
      setChartData(chartsRes.data);
      setParticipaciones(participacionesRes.data);

    } catch (error: any) {
      console.error("❌ Error detallado al cargar datos:", {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      });
      
      // Manejar errores específicos
      if (error.response?.status === 401) {
        toast.error("Sesión expirada. Redirigiendo al login...");
      } else if (error.response?.status === 403) {
        toast.error("No tienes permisos para acceder a esta información.");
      } else if (error.code === 'ERR_NETWORK') {
        toast.error("Error de conexión. Verifica que el servidor esté ejecutándose.");
      } else {
        toast.error("Error al cargar los datos del dashboard");
      }
      
      // Datos de respaldo en caso de error
      setStats({
        totalRespuestas: 0,
        usuariosActivos: 0,
        encuestasMasRespondidas: [],
        tiempoPromedioRespuesta: 0
      });

      setChartData({
        respuestasPorEncuesta: [],
        distribucionDemografica: [],
        respuestasPorDia: []
      });

      setParticipaciones([]);
    } finally {
      setLoading(false);
    }
  };

  const exportarPDF = async () => {
    try {
      console.log("📄 Exportando dashboard a PDF...");
      // Obtener datos actualizados para el PDF
      const response = await api.get("/dashboard/export-data");
      
      const { stats: pdfStats, participaciones: pdfParticipaciones } = response.data;
      
      const doc = new jsPDF();
      
      // Título
      doc.setFontSize(20);
      doc.setTextColor(33, 150, 243);
      doc.text("Dashboard de Administración", 20, 20);
      
      // Fecha
      doc.setFontSize(10);
      doc.setTextColor(100);
      doc.text(`Generado el: ${new Date().toLocaleDateString('es-ES')}`, 20, 30);
      
      // Estadísticas principales
      doc.setFontSize(14);
      doc.setTextColor(0);
      doc.text("Resumen de Estadísticas", 20, 45);
      
      doc.setFontSize(12);
      doc.text(`Total de Respuestas: ${pdfStats?.totalRespuestas || 0}`, 30, 55);
      doc.text(`Usuarios Activos: ${pdfStats?.usuariosActivos || 0}`, 30, 65);
      doc.text(`Tiempo Promedio de Respuesta: ${pdfStats?.tiempoPromedioRespuesta || 0} minutos`, 30, 75);
      
      // Tabla de participaciones
      const tableData = pdfParticipaciones.map((p: any) => [
        p.usuario,
        p.encuesta,
        p.fecha,
        `${p.duracion} min`
      ]);
      
      (doc as any).autoTable({
        startY: 90,
        head: [['Usuario', 'Encuesta', 'Fecha', 'Duración']],
        body: tableData,
        theme: 'grid',
        headStyles: { fillColor: [59, 130, 246] }
      });
      
      // Guardar PDF
      doc.save(`dashboard_${new Date().toISOString().split('T')[0]}.pdf`);
      toast.success("PDF exportado exitosamente");
      console.log("✅ PDF exportado correctamente");
    } catch (error) {
      console.error("❌ Error al exportar PDF:", error);
      toast.error("Error al exportar el PDF");
    }
  };

  // Mostrar loading mientras se verifica autenticación
  if (authLoading || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">
            {authLoading ? "Verificando permisos..." : "Cargando dashboard..."}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto mb-8"
      >
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Dashboard Administrativo</h1>
            <p className="text-gray-600 mt-1">Estadísticas y análisis del sistema</p>
          </div>
          <button
            onClick={exportarPDF}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors flex items-center gap-2"
          >
            <FaDownload /> Exportar PDF
          </button>
        </div>
      </motion.div>

      {/* KPI Cards */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl p-6 shadow-lg"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="bg-blue-100 p-3 rounded-lg">
              <FaPoll className="text-2xl text-blue-600" />
            </div>
            <span className="text-sm text-gray-500">Total</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-800">{stats?.totalRespuestas || 0}</h3>
          <p className="text-sm text-gray-600 mt-1">Respuestas totales</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-2xl p-6 shadow-lg"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="bg-green-100 p-3 rounded-lg">
              <FaUsers className="text-2xl text-green-600" />
            </div>
            <span className="text-sm text-gray-500">Activos</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-800">{stats?.usuariosActivos || 0}</h3>
          <p className="text-sm text-gray-600 mt-1">Usuarios activos</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-2xl p-6 shadow-lg"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="bg-purple-100 p-3 rounded-lg">
              <FaChartLine className="text-2xl text-purple-600" />
            </div>
            <span className="text-sm text-gray-500">Top</span>
          </div>
          <h3 className="text-xl font-bold text-gray-800">
            {stats?.encuestasMasRespondidas[0]?.titulo || "N/A"}
          </h3>
          <p className="text-sm text-gray-600 mt-1">Encuesta más popular</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-2xl p-6 shadow-lg"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="bg-orange-100 p-3 rounded-lg">
              <FaClock className="text-2xl text-orange-600" />
            </div>
            <span className="text-sm text-gray-500">Promedio</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-800">
            {stats?.tiempoPromedioRespuesta || 0} min
          </h3>
          <p className="text-sm text-gray-600 mt-1">Tiempo de respuesta</p>
        </motion.div>
      </div>

      {/* Gráficos */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Gráfico de barras */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-white rounded-2xl p-6 shadow-lg"
        >
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Respuestas por Encuesta</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData?.respuestasPorEncuesta}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="encuesta" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="respuestas" fill="#3B82F6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Gráfico de torta */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-white rounded-2xl p-6 shadow-lg"
        >
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Distribución por Edad</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={chartData?.distribucionDemografica}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => `${entry.name}: ${entry.value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {chartData?.distribucionDemografica.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Gráfico de línea */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="bg-white rounded-2xl p-6 shadow-lg lg:col-span-2"
        >
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Respuestas por Día</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData?.respuestasPorDia}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="fecha" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="respuestas" 
                stroke="#8B5CF6" 
                strokeWidth={3}
                dot={{ fill: '#8B5CF6', strokeWidth: 2, r: 6 }}
                activeDot={{ r: 8 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Tabla de participaciones */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="max-w-7xl mx-auto bg-white rounded-2xl shadow-lg overflow-hidden"
      >
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800">Participaciones Recientes</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Usuario</th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Encuesta</th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Fecha</th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Duración</th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-700">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {participaciones.map((participacion) => (
                <tr key={participacion.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 text-sm text-gray-900">{participacion.usuario}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">{participacion.encuesta}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{participacion.fecha}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{participacion.duracion} min</td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => setSelectedParticipacion(participacion)}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      Ver detalles
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>

      {/* Modal de detalles */}
      {selectedParticipacion && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
          onClick={() => setSelectedParticipacion(null)}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white rounded-2xl p-6 max-w-md w-full"
            onClick={(e) => e.stopPropagation()}
          >
            <h3 className="text-xl font-semibold mb-4">Detalles de Participación</h3>
            <div className="space-y-3">
              <div>
                <span className="text-gray-600">Usuario:</span>
                <p className="font-medium">{selectedParticipacion.usuario}</p>
              </div>
              <div>
                <span className="text-gray-600">Encuesta:</span>
                <p className="font-medium">{selectedParticipacion.encuesta}</p>
              </div>
              <div>
                <span className="text-gray-600">Fecha y hora:</span>
                <p className="font-medium">{selectedParticipacion.fecha}</p>
              </div>
              <div>
                <span className="text-gray-600">Duración:</span>
                <p className="font-medium">{selectedParticipacion.duracion} minutos</p>
              </div>
            </div>
            <button
              onClick={() => setSelectedParticipacion(null)}
              className="mt-6 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Cerrar
            </button>
          </motion.div>
        </div>
      )}
    </div>
  );
} 