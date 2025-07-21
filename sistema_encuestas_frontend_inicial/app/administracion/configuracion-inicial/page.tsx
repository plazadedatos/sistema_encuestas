"use client";

import { useState, useEffect } from "react";
import { FaCog, FaSave, FaToggleOn, FaToggleOff, FaGift, FaSpinner } from "react-icons/fa";
import api from "@/app/services/api";
import { useRouter } from "next/navigation";

interface ConfiguracionInicial {
  campos_activos: {
    fecha_nacimiento: boolean;
    sexo: boolean;
    localizacion: boolean;
  };
  puntos_completar_perfil: number;
  valores_defecto: {
    opciones_sexo: string[];
  };
}

export default function ConfiguracionInicialPage() {
  const router = useRouter();
  const [configuracion, setConfiguracion] = useState<ConfiguracionInicial>({
    campos_activos: {
      fecha_nacimiento: true,
      sexo: true,
      localizacion: true
    },
    puntos_completar_perfil: 5,
    valores_defecto: {
      opciones_sexo: ["M", "F", "Otro", "Prefiero no decir"]
    }
  });
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [mensaje, setMensaje] = useState("");

  useEffect(() => {
    cargarConfiguracion();
  }, []);

  const cargarConfiguracion = async () => {
    try {
      const response = await api.get("/admin/configuracion-inicial");
      setConfiguracion(response.data);
    } catch (error) {
      console.error("Error al cargar configuración:", error);
      // Si no existe configuración, usar valores por defecto
    } finally {
      setIsLoading(false);
    }
  };

  const toggleCampo = (campo: keyof typeof configuracion.campos_activos) => {
    setConfiguracion(prev => ({
      ...prev,
      campos_activos: {
        ...prev.campos_activos,
        [campo]: !prev.campos_activos[campo]
      }
    }));
  };

  const handlePuntosChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const valor = parseInt(e.target.value) || 0;
    setConfiguracion(prev => ({
      ...prev,
      puntos_completar_perfil: valor
    }));
  };

  const guardarConfiguracion = async () => {
    setIsSaving(true);
    setMensaje("");

    try {
      await api.post("/admin/configuracion-inicial", configuracion);
      setMensaje("Configuración guardada exitosamente");
      setTimeout(() => setMensaje(""), 3000);
    } catch (error) {
      console.error("Error al guardar configuración:", error);
      setMensaje("Error al guardar la configuración");
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="flex items-center gap-3">
          <FaSpinner className="animate-spin text-brand-vibrant text-2xl" />
          <span className="text-gray-600">Cargando configuración...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-br from-brand-vibrant to-brand-medium rounded-xl flex items-center justify-center">
              <FaCog className="text-white text-xl" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Configuración de Datos Iniciales</h1>
              <p className="text-gray-600">Gestiona los campos del perfil inicial de usuarios</p>
            </div>
          </div>
        </div>

        {/* Configuración de campos */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Campos del Perfil</h2>
          <div className="space-y-4">
            {/* Fecha de nacimiento */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex-1">
                <h3 className="font-medium text-gray-900">Fecha de Nacimiento</h3>
                <p className="text-sm text-gray-600">Los usuarios deberán ingresar su fecha de nacimiento</p>
              </div>
              <button
                onClick={() => toggleCampo('fecha_nacimiento')}
                className={`text-3xl transition-colors ${
                  configuracion.campos_activos.fecha_nacimiento 
                    ? 'text-brand-vibrant' 
                    : 'text-gray-400'
                }`}
              >
                {configuracion.campos_activos.fecha_nacimiento ? <FaToggleOn /> : <FaToggleOff />}
              </button>
            </div>

            {/* Sexo */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex-1">
                <h3 className="font-medium text-gray-900">Sexo</h3>
                <p className="text-sm text-gray-600">Los usuarios deberán seleccionar su sexo</p>
              </div>
              <button
                onClick={() => toggleCampo('sexo')}
                className={`text-3xl transition-colors ${
                  configuracion.campos_activos.sexo 
                    ? 'text-brand-vibrant' 
                    : 'text-gray-400'
                }`}
              >
                {configuracion.campos_activos.sexo ? <FaToggleOn /> : <FaToggleOff />}
              </button>
            </div>

            {/* Localización */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex-1">
                <h3 className="font-medium text-gray-900">Ciudad o Región</h3>
                <p className="text-sm text-gray-600">Los usuarios deberán seleccionar su ubicación</p>
              </div>
              <button
                onClick={() => toggleCampo('localizacion')}
                className={`text-3xl transition-colors ${
                  configuracion.campos_activos.localizacion 
                    ? 'text-brand-vibrant' 
                    : 'text-gray-400'
                }`}
              >
                {configuracion.campos_activos.localizacion ? <FaToggleOn /> : <FaToggleOff />}
              </button>
            </div>
          </div>
        </div>

        {/* Configuración de puntos */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Sistema de Puntos</h2>
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <label htmlFor="puntos" className="block text-sm font-medium text-gray-700 mb-2">
                Puntos por completar el perfil
              </label>
              <div className="flex items-center gap-3">
                <input
                  id="puntos"
                  type="number"
                  min="0"
                  max="100"
                  value={configuracion.puntos_completar_perfil}
                  onChange={handlePuntosChange}
                  className="w-24 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-vibrant focus:border-transparent"
                />
                <FaGift className="text-yellow-500 text-xl" />
                <span className="text-sm text-gray-600">puntos de recompensa</span>
              </div>
            </div>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Estos puntos se otorgarán automáticamente cuando el usuario complete su perfil inicial
          </p>
        </div>

        {/* Mensaje de estado */}
        {mensaje && (
          <div className={`p-4 rounded-lg mb-6 ${
            mensaje.includes('exitosamente') 
              ? 'bg-green-100 text-green-800 border border-green-200' 
              : 'bg-red-100 text-red-800 border border-red-200'
          }`}>
            {mensaje}
          </div>
        )}

        {/* Botones de acción */}
        <div className="flex gap-4">
          <button
            onClick={guardarConfiguracion}
            disabled={isSaving}
            className="flex-1 bg-gradient-to-r from-brand-vibrant to-brand-medium text-white py-3 px-6 rounded-lg font-medium hover:from-brand-dark hover:to-brand-vibrant transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {isSaving ? (
              <>
                <FaSpinner className="animate-spin" />
                <span>Guardando...</span>
              </>
            ) : (
              <>
                <FaSave />
                <span>Guardar Configuración</span>
              </>
            )}
          </button>
          <button
            onClick={() => router.push("/administracion/dashboard")}
            className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
          >
            Cancelar
          </button>
        </div>

        {/* Información adicional */}
        <div className="mt-6 bg-brand-light/10 border border-brand-light/30 rounded-lg p-4">
          <h3 className="text-sm font-medium text-brand-dark mb-2">
            Información importante
          </h3>
          <ul className="text-sm text-gray-700 space-y-1 list-disc list-inside">
            <li>Los cambios se aplicarán inmediatamente para nuevos usuarios</li>
            <li>Los usuarios existentes no se verán afectados</li>
            <li>Al menos un campo debe estar activo para recopilar datos</li>
            <li>Los puntos se otorgan solo una vez por usuario al completar el perfil</li>
          </ul>
        </div>
      </div>
    </div>
  );
} 