// components/GoogleLoginButton.tsx
'use client';

import { GoogleLogin } from '@react-oauth/google';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/authContext';
import { useState, useEffect } from 'react';
import { FaGoogle } from 'react-icons/fa';

export default function GoogleLoginButton() {
  const router = useRouter();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isGoogleConfigured, setIsGoogleConfigured] = useState(false);

  useEffect(() => {
    // Verificar si Google OAuth está configurado
    const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;
    setIsGoogleConfigured(!!clientId);
  }, []);

  const handleGoogleSuccess = async (credentialResponse: any) => {
    try {
      setLoading(true);
      setError('');

      // Enviar el token al backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/google`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id_token: credentialResponse.credential,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Error al iniciar sesión con Google');
      }

      // Guardar el token y la información del usuario
      localStorage.setItem('token', data.access_token);
      
      // Actualizar el contexto de autenticación
      login(data.access_token, data.usuario);

      // Redirigir según si es nuevo usuario o no
      if (data.usuario.es_nuevo) {
        router.push('/panel/bienvenida');
      } else {
        router.push('/panel');
      }
    } catch (error) {
      console.error('Error en login con Google:', error);
      setError(error instanceof Error ? error.message : 'Error al iniciar sesión');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleError = () => {
    setError('Error al conectar con Google');
  };

  // Si Google OAuth no está configurado, mostrar botón deshabilitado con mensaje
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
    <div className="w-full">
      {/* Contenedor personalizado para el botón de Google */}
      <div className="google-login-wrapper">
        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={handleGoogleError}
          theme="outline"
          size="large"
          text="continue_with"
          shape="rectangular"
          locale="es"
          width={400}
        />
      </div>
      
      {loading && (
        <div className="mt-3 text-center">
          <div className="inline-flex items-center text-sm text-gray-600">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900 mr-2"></div>
            <span>Conectando con Google...</span>
          </div>
        </div>
      )}
      
      {error && (
        <div className="mt-3 bg-red-50 border border-red-200 rounded-lg p-3">
          <p className="text-sm text-red-600 text-center">{error}</p>
          {error.includes("origin is not allowed") && (
            <p className="text-xs text-red-500 text-center mt-1">
              Configura http://localhost:3000 en Google Cloud Console
            </p>
          )}
        </div>
      )}

      <style jsx global>{`
        /* Estilos personalizados para el botón de Google */
        .google-login-wrapper {
          display: flex;
          justify-content: center;
          width: 100%;
        }

        .google-login-wrapper > div {
          width: 100% !important;
        }

        .google-login-wrapper iframe {
          width: 100% !important;
          max-width: 100% !important;
        }

        /* Mejorar la apariencia del botón */
        .google-login-wrapper > div > div {
          width: 100% !important;
          display: flex !important;
          justify-content: center !important;
        }
      `}</style>
    </div>
  );
} 