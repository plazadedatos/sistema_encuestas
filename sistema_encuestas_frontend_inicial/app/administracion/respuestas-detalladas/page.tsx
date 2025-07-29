'use client';

import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '@/context/authContext';
import api from '@/app/services/api';
import { FaDownload, FaTable } from 'react-icons/fa';
import {
  exportToPDF,
  exportToExcel,
  exportToCSV,
  exportToJSON,
} from '@/app/utils/exportUtils';

interface Encuesta {
  id: number;
  titulo: string;
  total_participaciones?: number;
}

interface RespuestaDetallada {
  participante_id: string;
  edad: string | number;
  sexo: string;
  localizacion: string;
  fecha: string;
  encuesta_id: number;
  encuesta_nom: string;
  respuestas: Record<string, string>;
}

export default function RespuestasDetalladasPage() {
  const { token } = useAuth();
  const [encuestas, setEncuestas] = useState<Encuesta[]>([]);
  const [selectedEncuesta, setSelectedEncuesta] = useState<number | null>(null);
  const [respuestas, setRespuestas] = useState<RespuestaDetallada[]>([]);
  const [loading, setLoading] = useState(false);

  const cargarEncuestas = async () => {
    try {
      const response = await api.get('/admin/encuestas-resumen');
      setEncuestas(response.data);
    } catch (error) {
      console.error('Error al cargar encuestas:', error);
    }
  };

  const cargarRespuestas = useCallback(async () => {
    if (!selectedEncuesta) return;

    setLoading(true);
    try {
      const response = await api.get(
        `/admin/respuestas-detalladas/${selectedEncuesta}`
      );
      setRespuestas(response.data);
    } catch (error) {
      console.error('Error al cargar respuestas:', error);
      setRespuestas([]);
    } finally {
      setLoading(false);
    }
  }, [selectedEncuesta]);

  useEffect(() => {
    cargarEncuestas();
  }, []);

  useEffect(() => {
    if (selectedEncuesta) {
      cargarRespuestas();
    }
  }, [cargarRespuestas, selectedEncuesta]);

  const obtenerColumnas = () => {
    if (respuestas.length === 0) return [];

    const respuestasKeys = Object.keys(respuestas[0].respuestas || {});
    return [
      'participante_id',
      'edad',
      'sexo',
      'localizacion',
      'fecha',
      'encuesta_id',
      'encuesta_nom',
      ...respuestasKeys,
    ];
  };

  const obtenerHeadersFormateados = () => {
    const columnas = obtenerColumnas();
    return columnas.map(col => {
      if (col === 'participante_id') return 'ID Participante';
      if (col === 'edad') return 'Edad';
      if (col === 'sexo') return 'Sexo';
      if (col === 'localizacion') return 'Localización';
      if (col === 'fecha') return 'Fecha';
      if (col === 'encuesta_id') return 'ID Encuesta';
      if (col === 'encuesta_nom') return 'Nombre Encuesta';
      if (col.startsWith('respuesta_'))
        return col.replace('respuesta_', 'Pregunta ');
      return col;
    });
  };

  const exportarDatos = (formato: 'pdf' | 'excel' | 'csv' | 'json') => {
    if (respuestas.length === 0) return;

    const columnas = obtenerColumnas();
    const headers = obtenerHeadersFormateados();

    const data = respuestas.map(r => {
      const row: (string | number)[] = [];
      columnas.forEach(col => {
        if (col === 'participante_id') row.push(r.participante_id);
        else if (col === 'edad') row.push(r.edad);
        else if (col === 'sexo') row.push(r.sexo);
        else if (col === 'localizacion') row.push(r.localizacion);
        else if (col === 'fecha') row.push(r.fecha);
        else if (col === 'encuesta_id') row.push(r.encuesta_id);
        else if (col === 'encuesta_nom') row.push(r.encuesta_nom);
        else row.push(r.respuestas[col] || '');
      });
      return row;
    });

    const filename = `respuestas_${respuestas[0]?.encuesta_nom.replace(/\s+/g, '_') || selectedEncuesta}`;

    switch (formato) {
      case 'pdf':
        exportToPDF(
          filename,
          headers,
          data,
          `Respuestas: ${respuestas[0]?.encuesta_nom || ''}`
        );
        break;
      case 'excel':
        exportToExcel(filename, headers, data, 'Respuestas Detalladas');
        break;
      case 'csv':
        exportToCSV({
          filename,
          data,
        });
        break;
      case 'json':
        exportToJSON({
          filename,
          data: respuestas,
        });
        break;
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 flex items-center">
        <FaTable className="mr-3 text-blue-600" />
        Respuestas Detalladas por Encuesta
      </h1>

      {/* Selector de encuesta */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Seleccionar Encuesta
        </label>
        <select
          value={selectedEncuesta || ''}
          onChange={e => setSelectedEncuesta(Number(e.target.value))}
          className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none transition-colors"
        >
          <option value="">-- Seleccione una encuesta --</option>
          {encuestas.map(enc => (
            <option key={enc.id} value={enc.id}>
              {enc.titulo} ({enc.total_participaciones || 0} participaciones)
            </option>
          ))}
        </select>
      </div>

      {/* Botones de exportación */}
      {selectedEncuesta && respuestas.length > 0 && (
        <div className="bg-white rounded-lg shadow p-4 mb-6 flex justify-between items-center">
          <div className="text-lg font-medium text-gray-700">
            Total de respuestas:{' '}
            <span className="text-blue-600 font-bold">{respuestas.length}</span>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => exportarDatos('excel')}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
            >
              <FaDownload />
              Excel
            </button>
            <button
              onClick={() => exportarDatos('csv')}
              className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors flex items-center gap-2"
            >
              <FaDownload />
              CSV
            </button>
            <button
              onClick={() => exportarDatos('pdf')}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
            >
              <FaDownload />
              PDF
            </button>
            <button
              onClick={() => exportarDatos('json')}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors flex items-center gap-2"
            >
              <FaDownload />
              JSON
            </button>
          </div>
        </div>
      )}

      {/* Tabla de resultados */}
      {loading ? (
        <div className="bg-white rounded-lg shadow p-10">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Cargando respuestas...</p>
          </div>
        </div>
      ) : selectedEncuesta && respuestas.length > 0 ? (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  {obtenerHeadersFormateados().map((header, idx) => (
                    <th
                      key={idx}
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {header}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {respuestas.map((respuesta, idx) => (
                  <tr key={idx} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {respuesta.participante_id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {respuesta.edad}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {respuesta.sexo}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {respuesta.localizacion}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {respuesta.fecha}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {respuesta.encuesta_id}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {respuesta.encuesta_nom}
                    </td>
                    {Object.keys(respuesta.respuestas || {}).map(key => (
                      <td key={key} className="px-6 py-4 text-sm text-gray-700">
                        <div
                          className="max-w-xs"
                          title={respuesta.respuestas[key]}
                        >
                          {respuesta.respuestas[key] || '-'}
                        </div>
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : selectedEncuesta ? (
        <div className="bg-white rounded-lg shadow p-10">
          <div className="text-center text-gray-500">
            <FaTable className="text-6xl mx-auto mb-4 text-gray-300" />
            <p className="text-lg">
              No hay respuestas registradas para esta encuesta
            </p>
          </div>
        </div>
      ) : (
        <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-10">
          <div className="text-center text-blue-600">
            <FaTable className="text-6xl mx-auto mb-4 text-blue-400" />
            <p className="text-lg font-medium">
              Seleccione una encuesta para ver las respuestas detalladas
            </p>
            <p className="text-sm mt-2 text-blue-500">
              La tabla mostrará todas las respuestas de los usuarios que
              completaron la encuesta seleccionada
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
