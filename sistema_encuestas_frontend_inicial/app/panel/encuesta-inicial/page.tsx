"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/authContext";
import { FaUser, FaGift, FaCheckCircle } from "react-icons/fa";
import api from "@/app/services/api";
import ciudadesParaguay from "@/data/ciudades-paraguay.json";

interface Ciudad {
  code: string;
  display: string;
}

export default function EncuestaInicialPage() {
  const router = useRouter();
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    fecha_nacimiento: "",
    sexo: "",
    localizacion: ""
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [isSuccess, setIsSuccess] = useState(false);
  const [ciudades, setCiudades] = useState<Ciudad[]>([]);

  useEffect(() => {
    // Cargar ciudades del JSON
    if (ciudadesParaguay && ciudadesParaguay.concept) {
      const ciudadesFormateadas = ciudadesParaguay.concept.map((ciudad: any) => ({
        code: ciudad.code,
        display: ciudad.display
      }));
      setCiudades(ciudadesFormateadas);
    }
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const response = await api.post("/perfil/completar", formData);
      setIsSuccess(true);
      
      // Redirigir al panel principal después de 3 segundos
      setTimeout(() => {
        router.push("/panel");
        router.refresh();
      }, 3000);
      
    } catch (error: any) {
      if (error.response?.data?.detail) {
        setError(error.response.data.detail);
      } else {
        setError("Error al completar el perfil. Por favor intenta nuevamente.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (isSuccess) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center">
          <div className="mx-auto h-20 w-20 bg-green-100 rounded-full flex items-center justify-center mb-6">
            <FaCheckCircle className="h-10 w-10 text-green-600" />
          </div>
          
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            ¡Perfil completado!
          </h1>
          
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
            <div className="flex items-center justify-center mb-2">
              <FaGift className="h-6 w-6 text-green-600 mr-2" />
              <span className="text-lg font-semibold text-green-800">
                ¡Has ganado 5 puntos!
              </span>
            </div>
            <p className="text-sm text-green-700">
              Gracias por completar tu perfil. Estos puntos ya están disponibles en tu cuenta.
            </p>
          </div>
          
          <p className="text-gray-600 mb-6">
            Serás redirigido al panel principal en unos segundos...
          </p>
          
          <div className="flex justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-white rounded-2xl shadow-xl overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-6 text-white">
          <div className="flex items-center">
            <div className="h-12 w-12 bg-white/20 rounded-full flex items-center justify-center mr-4">
              <FaUser className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">¡Bienvenido, {user?.nombre}!</h1>
              <p className="text-blue-100">Completa tu perfil para comenzar</p>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-8">
          <div className="mb-6">
            <div className="flex items-center justify-center mb-4">
              <div className="bg-yellow-100 rounded-full p-3">
                <FaGift className="h-6 w-6 text-yellow-600" />
              </div>
            </div>
            <h2 className="text-xl font-semibold text-center text-gray-900 mb-2">
              Completa tu perfil y gana 5 puntos
            </h2>
            <p className="text-center text-gray-600">
              Necesitamos algunos datos adicionales para personalizar tu experiencia
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Fecha de nacimiento */}
            <div>
              <label htmlFor="fecha_nacimiento" className="block text-sm font-medium text-gray-700 mb-2">
                Fecha de nacimiento *
              </label>
              <input
                type="date"
                id="fecha_nacimiento"
                name="fecha_nacimiento"
                required
                max={new Date().toISOString().split('T')[0]}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                value={formData.fecha_nacimiento}
                onChange={handleInputChange}
              />
            </div>

            {/* Sexo */}
            <div>
              <label htmlFor="sexo" className="block text-sm font-medium text-gray-700 mb-2">
                Sexo *
              </label>
              <select
                id="sexo"
                name="sexo"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                value={formData.sexo}
                onChange={handleInputChange}
              >
                <option value="">Selecciona una opción</option>
                <option value="M">Masculino</option>
                <option value="F">Femenino</option>
                <option value="Otro">Otro</option>
                <option value="Prefiero no decir">Prefiero no decir</option>
              </select>
            </div>

            {/* Localización */}
            <div>
              <label htmlFor="localizacion" className="block text-sm font-medium text-gray-700 mb-2">
                Ciudad o región *
              </label>
              <select
                id="localizacion"
                name="localizacion"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                value={formData.localizacion}
                onChange={handleInputChange}
              >
                <option value="">Selecciona una ciudad</option>
                {ciudades.map((ciudad) => (
                  <option key={ciudad.code} value={ciudad.code}>
                    {ciudad.display}
                  </option>
                ))}
              </select>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}

            {/* Información sobre los puntos */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start">
                <FaGift className="h-5 w-5 text-blue-600 mr-3 mt-0.5" />
                <div>
                  <h4 className="text-sm font-medium text-blue-900">
                    Sobre tus puntos de bienvenida
                  </h4>
                  <p className="text-sm text-blue-700 mt-1">
                    Al completar tu perfil recibirás 5 puntos que podrás usar para canjear premios. 
                    Solo se otorgan una vez por usuario.
                  </p>
                </div>
              </div>
            </div>

            {/* Submit button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Completando perfil...
                </span>
              ) : (
                "Completar perfil y ganar 5 puntos"
              )}
            </button>

            <p className="text-xs text-gray-500 text-center">
              * Campos obligatorios. Esta información nos ayuda a personalizar tu experiencia.
            </p>
          </form>
        </div>
      </div>
    </div>
  );
} 