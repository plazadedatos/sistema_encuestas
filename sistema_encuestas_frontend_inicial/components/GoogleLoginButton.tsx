// components/GoogleLoginButton.tsx
'use client';

import { GoogleLogin } from '@react-oauth/google';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/authContext';
import { useState, useEffect, useRef } from 'react';
import { FaGoogle } from 'react-icons/fa';
import api from '@/app/services/api';

export default function GoogleLoginButton() {
  const { loginWithGoogle } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isGoogleConfigured, setIsGoogleConfigured] = useState(false);
  const [showSlowMessage, setShowSlowMessage] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const slowRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;
    setIsGoogleConfigured(!!clientId);
  }, []);

  const handleGoogleSuccess = async (credentialResponse: any) => {
    setLoading(true);
    setError('');
    setShowSlowMessage(false);

    // Mensaje si tarda más de 5 segundos
    slowRef.current = setTimeout(() => setShowSlowMessage(true), 5000);

    // Timeout total de 8 segundos
    timeoutRef.current = setTimeout(() => {
      setLoading(false);
      setShowSlowMessage(false);
      setError('La validación con Google está tardando demasiado. Por favor, inténtalo de nuevo.');
    }, 8000);

    try {
      const controller = new AbortController();
      const idTimeout = setTimeout(() => controller.abort(), 8000);
      const response = await api.post('/auth/google', { 
        id_token: credentialResponse.credential 
      }, {
        signal: controller.signal,
      });
      clearTimeout(idTimeout);
      clearTimeout(timeoutRef.current!);
      clearTimeout(slowRef.current!);
      setShowSlowMessage(false);

      const data = response.data;
      const success = await loginWithGoogle(data.access_token, data.usuario);
      if (!success) {
        throw new Error('Error al procesar el login con Google');
      }
    } catch (error: any) {
      if (error.name === 'AbortError') {
        setError('La validación con Google está tardando demasiado. Por favor, inténtalo de nuevo.');
      } else {
        setError(error instanceof Error ? error.message : 'Error al iniciar sesión');
      }
    } finally {
      setLoading(false);
      setShowSlowMessage(false);
      clearTimeout(timeoutRef.current!);
      clearTimeout(slowRef.current!);
    }
  };

  const handleGoogleError = () => {
    setError('Error al conectar con Google');
  };

  if (!isGoogleConfigured) {
    return (
      <div className="w-full">
        <button
          disabled
          className="w-full flex items-center justify-center py-3 px-4 border border-gray-300 text-gray-500 bg-gray-50 font-medium rounded-lg cursor-not-allowed"
        >
          <FaGoogle className="w-5 h-5 mr-3" />
          <span>Continuar con Google</span>
        </button>
        <p className="text-xs text-center text-gray-500 mt-2">
          Google OAuth no configurado
        </p>
      </div>
    );
  }

  return (
    <div className="w-full flex justify-center">
      <div className="google-login-wrapper w-full max-w-sm">
        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={handleGoogleError}
          theme="outline"
          size="large"
          text="continue_with"
          shape="rectangular"
          locale="es"
          width="100%"
        />
      </div>
      {loading && (
        <div className="mt-3 text-center">
          <div className="inline-flex items-center text-sm text-gray-600">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900 mr-2"></div>
            <span>Conectando con Google...</span>
          </div>
          {showSlowMessage && (
            <div className="mt-2 text-xs text-yellow-600">La validación está tardando más de lo normal, por favor espera o reintenta.</div>
          )}
        </div>
      )}
      {error && (
        <div className="mt-3 bg-red-50 border border-red-200 rounded-lg p-3">
          <p className="text-sm text-red-600 text-center">{error}</p>
          <button
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 mx-auto block"
            onClick={() => { setError(''); setLoading(false); setShowSlowMessage(false); }}
          >
            Reintentar
          </button>
        </div>
      )}
      <style jsx global>{`
        .google-login-wrapper {
          display: flex;
          justify-content: center;
          width: 100%;
        }
        .google-login-wrapper > div {
          width: 100% !important;
          display: flex !important;
          justify-content: center !important;
        }
        .google-login-wrapper iframe {
          width: 100% !important;
          max-width: 100% !important;
          border-radius: 8px !important;
        }
        .google-login-wrapper > div > div {
          width: 100% !important;
          display: flex !important;
          justify-content: center !important;
        }
        .google-login-wrapper > div > div > div {
          width: 100% !important;
          display: flex !important;
          justify-content: center !important;
        }
      `}</style>
    </div>
  );
} 