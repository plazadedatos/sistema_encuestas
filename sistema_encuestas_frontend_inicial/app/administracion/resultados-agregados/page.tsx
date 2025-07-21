"use client";

import { useState, useEffect, useCallback } from "react";
import { useAuth } from "@/context/authContext";
import api from "@/app/services/api";
import {
  BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts";
import { FaDownload, FaChartBar, FaList } from "react-icons/fa";
import { exportToPDF, exportToExcel, exportToCSV, exportToJSON, objectsToTableData } from "@/app/utils/exportUtils";

interface Encuesta {
  id: number;
  titulo: string;
  total_participaciones?: number;
}

interface EstadisticaPregunta {
  id: number;
  tipo: string;
  pregunta: string;
  estadisticas?: Record<string, number>;
  respuestas_texto?: string[];
}

interface ResultadosData {
  encuesta: Encuesta;
  preguntas: EstadisticaPregunta[];
}

const COLORS = ['#3B82F6', '#8B5CF6', '#EC4899', '#10B981', '#F59E0B', '#EF4444', '#6366F1', '#14B8A6'];

export default function ResultadosAgregadosPage() {
  const { token } = useAuth();
  const [encuestas, setEncuestas] = useState<Encuesta[]>([]);
  const [selectedEncuesta, setSelectedEncuesta] = useState<number | null>(null);
  const [resultados, setResultados] = useState<ResultadosData | null>(null);
  const [loading, setLoading] = useState(false);
  const [vistaGrafico, setVistaGrafico] = useState(true);

  useEffect(() => {
    cargarEncuestas();
  }, []);

  const cargarEncuestas = async () => {
    try {
      const response = await api.get("/admin/encuestas-resumen");
      setEncuestas(response.data);
      if (response.data.length > 0) {
        setSelectedEncuesta(response.data[0].id);
      }
    } catch (error) {
      console.error("Error al cargar encuestas:", error);
    }
  };

  const cargarResultados = useCallback(async () => {
    if (!selectedEncuesta) return;
    
    setLoading(true);
    try {
      const response = await api.get(`/admin/estadisticas-por-encuesta/${selectedEncuesta}`);
      setResultados(response.data);
    } catch (error) {
      console.error("Error al cargar resultados:", error);
    } finally {
      setLoading(false);
    }
  }, [selectedEncuesta]);

  useEffect(() => {
    if (selectedEncuesta) {
      cargarResultados();
    }
  }, [cargarResultados, selectedEncuesta]);

  const prepararDatosParaGrafico = (estadisticas: Record<string, number>) => {
    return Object.entries(estadisticas).map(([opcion, cantidad]) => ({
      name: opcion,
      value: cantidad
    }));
  };

  const exportarDatos = (formato: 'pdf' | 'excel' | 'csv' | 'json') => {
    if (!resultados) return;

    const datosExportacion = resultados.preguntas.map(pregunta => {
      if (pregunta.tipo === 'opcion_multiple' && pregunta.estadisticas) {
        return {
          pregunta: pregunta.pregunta,
          tipo: 'Opción Múltiple',
          resultados: Object.entries(pregunta.estadisticas)
            .map(([opcion, cantidad]) => `${opcion}: ${cantidad}`)
            .join(', ')
        };
      } else {
        return {
          pregunta: pregunta.pregunta,
          tipo: 'Texto Libre',
          resultados: `${pregunta.respuestas_texto?.length || 0} respuestas`
        };
      }
    });

    const headers = ['Pregunta', 'Tipo', 'Resultados'];
    const data = objectsToTableData(datosExportacion, ['pregunta', 'tipo', 'resultados']);

    switch (formato) {
      case 'pdf':
        exportToPDF({
          filename: `resultados_${resultados.encuesta.titulo}`,
          headers,
          data,
          title: `Resultados: ${resultados.encuesta.titulo}`
        });
        break;
      case 'excel':
        exportToExcel({
          filename: `resultados_${resultados.encuesta.titulo}`,
          headers,
          data,
          title: 'Resultados'
        });
        break;
      case 'csv':
        exportToCSV({
          filename: `resultados_${resultados.encuesta.titulo}`,
          headers,
          data
        });
        break;
      case 'json':
        exportToJSON({
          filename: `resultados_${resultados.encuesta.titulo}`,
          data: resultados
        });
        break;
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Resultados Agregados por Encuesta</h1>

      {/* Selector de encuesta */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Seleccionar Encuesta
        </label>
        <select
          value={selectedEncuesta || ''}
          onChange={(e) => setSelectedEncuesta(Number(e.target.value))}
          className="w-full p-2 border rounded-lg"
        >
          <option value="">Seleccione una encuesta</option>
          {encuestas.map(enc => (
            <option key={enc.id} value={enc.id}>
              {enc.titulo} ({enc.total_participaciones} participaciones)
            </option>
          ))}
        </select>
      </div>

      {/* Controles */}
      <div className="bg-white rounded-lg shadow p-4 mb-6 flex justify-between items-center">
        <div className="flex gap-2">
          <button
            onClick={() => setVistaGrafico(true)}
            className={`px-4 py-2 rounded ${vistaGrafico ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          >
            <FaChartBar className="inline mr-2" />
            Vista Gráfica
          </button>
          <button
            onClick={() => setVistaGrafico(false)}
            className={`px-4 py-2 rounded ${!vistaGrafico ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          >
            <FaList className="inline mr-2" />
            Vista Lista
          </button>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => exportarDatos('pdf')}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            <FaDownload className="inline mr-2" />
            PDF
          </button>
          <button
            onClick={() => exportarDatos('excel')}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            <FaDownload className="inline mr-2" />
            Excel
          </button>
          <button
            onClick={() => exportarDatos('csv')}
            className="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700"
          >
            <FaDownload className="inline mr-2" />
            CSV
          </button>
          <button
            onClick={() => exportarDatos('json')}
            className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
          >
            <FaDownload className="inline mr-2" />
            JSON
          </button>
        </div>
      </div>

      {/* Resultados */}
      {loading ? (
        <div className="text-center py-10">Cargando resultados...</div>
      ) : resultados ? (
        <div className="space-y-6">
          {resultados.preguntas.map((pregunta, index) => (
            <div key={pregunta.id} className="bg-white rounded-lg shadow p-6">
              <h3 className="text-xl font-semibold mb-4">
                {index + 1}. {pregunta.pregunta}
              </h3>

              {pregunta.tipo === 'opcion_multiple' && pregunta.estadisticas ? (
                vistaGrafico ? (
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Gráfico de barras */}
                    <div>
                      <h4 className="text-sm font-medium text-gray-600 mb-2">Distribución de respuestas</h4>
                      <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={prepararDatosParaGrafico(pregunta.estadisticas)}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" />
                          <YAxis />
                          <Tooltip />
                          <Bar dataKey="value" fill="#3B82F6" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>

                    {/* Gráfico de dona */}
                    <div>
                      <h4 className="text-sm font-medium text-gray-600 mb-2">Porcentaje</h4>
                      <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                          <Pie
                            data={prepararDatosParaGrafico(pregunta.estadisticas)}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={100}
                            paddingAngle={5}
                            dataKey="value"
                            label={({name, percent}) => `${name}: ${((percent || 0) * 100).toFixed(0)}%`}
                          >
                            {prepararDatosParaGrafico(pregunta.estadisticas).map((entry, idx) => (
                              <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
                            ))}
                          </Pie>
                          <Tooltip />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Opción</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Respuestas</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Porcentaje</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {Object.entries(pregunta.estadisticas).map(([opcion, cantidad]) => {
                          const total = Object.values(pregunta.estadisticas!).reduce((a, b) => a + b, 0);
                          const porcentaje = total > 0 ? (cantidad / total * 100).toFixed(1) : '0';
                          return (
                            <tr key={opcion}>
                              <td className="px-6 py-4 whitespace-nowrap">{opcion}</td>
                              <td className="px-6 py-4 whitespace-nowrap">{cantidad}</td>
                              <td className="px-6 py-4 whitespace-nowrap">{porcentaje}%</td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                )
              ) : (
                <div>
                  <h4 className="text-sm font-medium text-gray-600 mb-2">
                    Respuestas de texto ({pregunta.respuestas_texto?.length || 0} respuestas)
                  </h4>
                  <div className="max-h-64 overflow-y-auto border rounded p-3">
                    {pregunta.respuestas_texto?.map((respuesta, idx) => (
                      <div key={idx} className="py-2 border-b last:border-0">
                        {respuesta}
                      </div>
                    )) || <p className="text-gray-500">No hay respuestas</p>}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-10 text-gray-500">
          Seleccione una encuesta para ver los resultados
        </div>
      )}
    </div>
  );
} 