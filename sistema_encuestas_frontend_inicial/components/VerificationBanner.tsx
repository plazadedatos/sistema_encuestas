'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/authContext';
import { FaEnvelope, FaTimes, FaCheckCircle } from 'react-icons/fa';
import api from '@/app/services/api';
import { toast } from 'react-toastify';

export default function VerificationBanner() {
  const { user } = useAuth();
  const [isVisible, setIsVisible] = useState(true);
  const [isResending, setIsResending] = useState(false);

  // Debug: Log del estado del usuario
  useEffect(() => {
    if (user) {
      console.log('🔍 VerificationBanner - Estado del usuario:', {
        email: user.email,
        email_verificado: user.email_verificado,
        tipo_valor: typeof user.email_verificado
      });
    }
  }, [user]);

  // No mostrar el banner si:
  // 1. No hay usuario
  // 2. El email está verificado (true o 'true' como string)
  // 3. El usuario lo ocultó manualmente
  const emailVerificado = user?.email_verificado === true || String(user?.email_verificado) === 'true';
  
  if (!user || emailVerificado || !isVisible) {
    return null;
  }

  const handleResendVerification = async () => {
    if (!user?.email) return;
    
    setIsResending(true);
    try {
      await api.post('/auth/reenviar-verificacion', { email: user.email });
      toast.success('📧 Correo de verificación enviado. Revisa tu bandeja de entrada.');
    } catch (error) {
      toast.error('No se pudo enviar el correo. Intenta más tarde.');
    } finally {
      setIsResending(false);
    }
  };

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mx-4 mt-4 relative">
      {/* Botón para cerrar */}
      <button
        onClick={() => setIsVisible(false)}
        className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 transition-colors"
      >
        <FaTimes className="w-4 h-4" />
      </button>

      <div className="flex items-start space-x-3 pr-8">
        <div className="bg-blue-100 rounded-full p-2 flex-shrink-0">
          <FaEnvelope className="w-5 h-5 text-blue-600" />
        </div>
        
        <div className="flex-1">
          <h4 className="text-sm font-semibold text-blue-900 mb-1">
            📧 Verificación de email (opcional)
          </h4>
          <p className="text-sm text-blue-700 mb-3">
            Tu cuenta funciona perfectamente, pero puedes verificar tu email para mayor seguridad y recibir notificaciones importantes.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-2">
            <button
              onClick={handleResendVerification}
              disabled={isResending}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isResending ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Enviando...
                </>
              ) : (
                <>
                  <FaEnvelope className="w-4 h-4 mr-2" />
                  Verificar ahora
                </>
              )}
            </button>
            
            <button
              onClick={() => setIsVisible(false)}
              className="text-sm text-blue-600 hover:text-blue-700 px-4 py-2 transition-colors"
            >
              Recordar más tarde
            </button>
          </div>
        </div>
      </div>
      
      {/* Indicador de beneficios */}
      <div className="mt-3 pt-3 border-t border-blue-200">
        <p className="text-xs text-blue-600 flex items-center">
          <FaCheckCircle className="w-3 h-3 mr-1" />
          Beneficios: Recuperación de cuenta, notificaciones importantes y mayor seguridad
        </p>
      </div>
    </div>
  );
} 