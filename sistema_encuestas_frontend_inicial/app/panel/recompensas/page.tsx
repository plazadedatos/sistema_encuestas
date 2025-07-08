"use client";
import { useEffect, useState } from "react";

import { getPremios, canjearPremio, getHistorialCanjes } from "../../services/encuestas";
import { useAuth } from "../../../context/authContext";
import api from "../../services/api";
import { Premio, PuntosData, Canje, EstadoCanje } from "@/types";

export default function RecompensasPage() {
  const { token } = useAuth();
  const [premios, setPremios] = useState<Premio[]>([]);
  const [puntos, setPuntos] = useState<PuntosData | null>(null);
  const [historial, setHistorial] = useState<Canje[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [canjeando, setCanjeando] = useState(false);
  const [idCanjeando, setIdCanjeando] = useState<number | null>(null);
  const [mostrarHistorial, setMostrarHistorial] = useState(false);

  useEffect(() => {
    if (token) {
      cargarDatos();
    }
  }, [token]);

  const cargarDatos = async () => {
    if (!token) {
      setError("No se encontró token de autenticación");
      setLoading(false);
      return;
    }
    
    try {
      // Cargar premios
      const resPremios = await getPremios(token);
      setPremios(resPremios.data);
      
      // Cargar puntos del usuario
      const resPuntos = await api.get("/usuario/me/puntos", {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPuntos(resPuntos.data);
      
      // Cargar historial
      const resHistorial = await getHistorialCanjes(token);
      setHistorial(resHistorial.data);
    } catch (e) {
      setError("Error al cargar datos");
    } finally {
      setLoading(false);
    }
  };

  const handleCanjear = async (premio: Premio) => {
    if (!token) {
      setError("No se encontró token de autenticación");
      return;
    }

    if (!puntos || puntos.puntos_disponibles < premio.costo_puntos) {
      setError(`Puntos insuficientes. Tienes ${puntos?.puntos_disponibles || 0} y necesitas ${premio.costo_puntos}`);
      return;
    }

    setCanjeando(true);
    setIdCanjeando(premio.id_premio);
    setMensaje("");
    setError("");
    
    try {
      await canjearPremio({ 
        id_premio: premio.id_premio, 
        acepta_terminos: true 
      }, token);
      
      setMensaje("¡Canje realizado con éxito! 🎉");
      
      // Actualizar puntos
      setPuntos(prev => prev ? {
        ...prev,
        puntos_disponibles: prev.puntos_disponibles - premio.costo_puntos,
        puntos_canjeados: prev.puntos_canjeados + premio.costo_puntos
      } : null);
      
      // Recargar datos
      cargarDatos();
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Error al canjear premio");
    } finally {
      setCanjeando(false);
      setIdCanjeando(null);
    }
  };

  const getEstadoColor = (estado: EstadoCanje): string => {
    switch(estado) {
      case 'entregado': return 'bg-green-100 text-green-800';
      case 'aprobado': return 'bg-blue-100 text-blue-800';
      case 'pendiente': return 'bg-yellow-100 text-yellow-800';
      case 'rechazado': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) return <div className="p-8">Cargando premios...</div>;

  return (
    <div className="max-w-7xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Tus Recompensas</h1>
        <button
          onClick={() => setMostrarHistorial(!mostrarHistorial)}
          className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 transition-colors"
        >
          {mostrarHistorial ? "Ver Premios" : "Ver Historial"}
        </button>
      </div>

      {/* Tarjeta de puntos */}
      {puntos && (
        <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg p-6 mb-6 shadow-lg">
          <h2 className="text-xl font-semibold mb-2">Tus Puntos</h2>
          <div className="flex justify-between items-center">
            <div>
              <p className="text-3xl font-bold">{puntos.puntos_disponibles}</p>
              <p className="text-sm opacity-90">Puntos disponibles</p>
            </div>
            <div className="text-right">
              <p className="text-lg">{puntos.puntos_canjeados}</p>
              <p className="text-sm opacity-90">Puntos canjeados</p>
            </div>
          </div>
        </div>
      )}

      {mensaje && <div className="bg-green-100 text-green-700 p-4 rounded mb-4">{mensaje}</div>}
      {error && <div className="bg-red-100 text-red-700 p-4 rounded mb-4">{error}</div>}

      {!mostrarHistorial ? (
        // Vista de premios disponibles
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {premios.filter(p => p.esta_disponible).map((premio) => (
            <div key={premio.id_premio} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
              {premio.imagen_url && (
                <img 
                  src={premio.imagen_url} 
                  alt={premio.nombre} 
                  className="w-full h-48 object-cover" 
                />
              )}
              <div className="p-4">
                <h2 className="font-bold text-xl mb-2">{premio.nombre}</h2>
                <p className="text-gray-600 text-sm mb-4">{premio.descripcion}</p>
                
                <div className="flex justify-between items-center mb-4">
                  <div>
                    <span className="text-2xl font-bold text-purple-600">{premio.costo_puntos}</span>
                    <span className="text-sm text-gray-500 ml-1">puntos</span>
                  </div>
                  <div className="text-sm text-gray-500">
                    Stock: {premio.stock_disponible ?? 'Ilimitado'}
                  </div>
                </div>
                
                <button
                  className={`w-full py-2 px-4 rounded font-semibold transition-colors ${
                    !puntos || puntos.puntos_disponibles < premio.costo_puntos
                      ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                      : canjeando && idCanjeando === premio.id_premio
                      ? 'bg-gray-400 text-gray-600'
                      : 'bg-purple-600 text-white hover:bg-purple-700'
                  }`}
                  disabled={!puntos || puntos.puntos_disponibles < premio.costo_puntos || canjeando}
                  onClick={() => handleCanjear(premio)}
                >
                  {canjeando && idCanjeando === premio.id_premio 
                    ? "Canjeando..." 
                    : !puntos || puntos.puntos_disponibles < premio.costo_puntos
                    ? "Puntos insuficientes"
                    : "Canjear"}
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        // Vista de historial
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Premio
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Puntos
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Fecha
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estado
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {historial.map((canje) => (
                <tr key={canje.id_canje}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    Premio #{canje.id_premio}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {canje.puntos_utilizados}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {new Date(canje.fecha_solicitud).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getEstadoColor(canje.estado)}`}>
                      {canje.estado}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
