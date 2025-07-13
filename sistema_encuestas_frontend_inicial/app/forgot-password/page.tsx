"use client";

import { useState } from "react";
import Link from "next/link";
import { FaEnvelope, FaArrowLeft, FaSpinner, FaCheckCircle } from "react-icons/fa";
import { toast } from "react-toastify";
import api from "@/app/services/api";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isEmailSent, setIsEmailSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email) {
      toast.error("Por favor ingresa tu correo electrónico");
      return;
    }

    setIsLoading(true);
    
    try {
      const response = await api.post("/auth/forgot-password", { email });
      
      if (response.data.success) {
        setIsEmailSent(true);
        toast.success("Correo de recuperación enviado. Revisa tu bandeja de entrada.");
      }
    } catch (error: any) {
      console.error("Error al enviar correo de recuperación:", error);
      toast.error(error.response?.data?.detail || "Error al enviar el correo de recuperación");
    } finally {
      setIsLoading(false);
    }
  };

  if (isEmailSent) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <div className="bg-green-100 p-4 rounded-full">
                <FaCheckCircle className="w-12 h-12 text-green-600" />
              </div>
            </div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              ¡Correo enviado!
            </h2>
            <p className="text-sm text-gray-600 mb-6">
              Te hemos enviado un correo con las instrucciones para restablecer tu contraseña a <strong>{email}</strong>
            </p>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <p className="text-sm text-blue-800">
                <strong>⚠️ Importante:</strong> El enlace expirará en 15 minutos por razones de seguridad.
              </p>
            </div>
            <div className="space-y-4">
              <button
                onClick={() => {
                  setIsEmailSent(false);
                  setEmail("");
                }}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
              >
                Enviar otro correo
              </button>
              <Link
                href="/login"
                className="w-full bg-gray-100 text-gray-700 py-3 px-4 rounded-lg font-medium hover:bg-gray-200 transition-colors block text-center"
              >
                Volver al login
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 rounded-2xl shadow-lg">
              <FaEnvelope className="w-12 h-12 text-white" />
            </div>
          </div>
          <h2 className="text-3xl font-bold text-gray-900">
            ¿Olvidaste tu contraseña?
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Ingresa tu correo electrónico y te enviaremos las instrucciones para restablecerla
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Correo electrónico
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <FaEnvelope className="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="appearance-none relative block w-full pl-10 pr-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm transition-colors"
                placeholder="tu@ejemplo.com"
                disabled={isLoading}
              />
            </div>
          </div>

          <div className="space-y-4">
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <FaSpinner className="animate-spin mr-2" />
                  Enviando...
                </>
              ) : (
                'Enviar correo de recuperación'
              )}
            </button>

            <Link
              href="/login"
              className="group relative w-full flex justify-center py-3 px-4 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
            >
              <FaArrowLeft className="mr-2" />
              Volver al login
            </Link>
          </div>
        </form>

        <div className="text-center">
          <p className="text-sm text-gray-600">
            ¿No tienes una cuenta?{' '}
            <Link href="/registro" className="font-medium text-blue-600 hover:text-blue-500">
              Regístrate aquí
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
} 