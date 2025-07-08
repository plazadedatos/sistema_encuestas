"use client";

import { useState } from 'react';
import api from '@/app/services/api';

export default function TestCorsPage() {
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testPublicEndpoint = async () => {
    setLoading(true);
    setResult('Probando endpoint público...');
    
    try {
      const response = await fetch('http://localhost:8000/api/ping');
      const data = await response.json();
      
      setResult(`✅ CORS funciona correctamente: ${JSON.stringify(data, null, 2)}`);
      console.log("✅ Respuesta del servidor:", data);
    } catch (error: any) {
      setResult(`❌ Error CORS: ${error.message}`);
      console.error("❌ Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const testProtectedEndpoint = async () => {
    setLoading(true);
    setResult('Probando endpoint protegido...');
    
    try {
      const response = await api.get('/dashboard/stats');
      setResult(`✅ Endpoint protegido funciona: ${JSON.stringify(response.data, null, 2)}`);
      console.log("✅ Respuesta del endpoint protegido:", response.data);
    } catch (error: any) {
      setResult(`❌ Error en endpoint protegido: ${error.message} (Status: ${error.response?.status})`);
      console.error("❌ Error en endpoint protegido:", error);
    } finally {
      setLoading(false);
    }
  };

  const testTokenInfo = () => {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    
    setResult(`Token: ${token ? 'Presente' : 'Ausente'}\nUsuario: ${user ? 'Presente' : 'Ausente'}\n\n${token ? `Token: ${token.substring(0, 50)}...` : 'No hay token'}`);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Pruebas de CORS y Autenticación</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <button
            onClick={testPublicEndpoint}
            disabled={loading}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
          >
            Probar Endpoint Público
          </button>
          
          <button
            onClick={testProtectedEndpoint}
            disabled={loading}
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 disabled:opacity-50"
          >
            Probar Endpoint Protegido
          </button>
          
          <button
            onClick={testTokenInfo}
            disabled={loading}
            className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600 disabled:opacity-50"
          >
            Ver Info de Token
          </button>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Resultado:</h2>
          <pre className="bg-gray-100 p-4 rounded overflow-auto max-h-96">
            {loading ? 'Cargando...' : result || 'Haz clic en un botón para probar'}
          </pre>
        </div>

        <div className="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h3 className="font-semibold text-yellow-800 mb-2">Instrucciones:</h3>
          <ul className="list-disc list-inside text-yellow-700 space-y-1">
            <li><strong>Endpoint Público:</strong> Debe funcionar sin token (prueba CORS)</li>
            <li><strong>Endpoint Protegido:</strong> Requiere estar logueado como administrador</li>
            <li><strong>Info de Token:</strong> Muestra si hay datos de sesión guardados</li>
          </ul>
        </div>
      </div>
    </div>
  );
} 