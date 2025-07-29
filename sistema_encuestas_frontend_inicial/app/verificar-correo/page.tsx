'use client';

import { useEffect, useState, useCallback, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { FaCheckCircle, FaTimesCircle, FaInfoCircle } from 'react-icons/fa';
import api from '@/app/services/api';

function VerificarCorreoContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [verificando, setVerificando] = useState(true);
  const [mensaje, setMensaje] = useState('');
  const [exitoso, setExitoso] = useState(false);
  const [email, setEmail] = useState('');
  const [esEmailYaVerificado, setEsEmailYaVerificado] = useState(false);

  const verificarEmail = useCallback(
    async (token: string) => {
      try {
        const response = await api.get(`/auth/verificar-correo?token=${token}`);
        const data = response.data;

        if (response.status === 200) {
          // Verificar el estado específico de la respuesta
          if (data.estado === 'verificado_exitosamente') {
            setExitoso(true);
            setMensaje('¡Email verificado exitosamente!');
            setEmail(data.email || '');

            // Redirigir al panel después de 3 segundos
            setTimeout(() => {
              router.push('/panel');
            }, 3000);
          } else if (data.estado === 'ya_verificado') {
            setExitoso(true);
            setEsEmailYaVerificado(true);
            setMensaje(
              data.mensaje || 'Este email ya fue verificado anteriormente'
            );
            setEmail(data.email || '');

            // Redirigir al panel después de 2 segundos
            setTimeout(() => {
              router.push('/panel');
            }, 2000);
          } else {
            // Caso genérico de éxito
            setExitoso(true);
            setMensaje(data.mensaje || 'Email verificado');
            setEmail(data.email || '');

            setTimeout(() => {
              router.push('/panel');
            }, 3000);
          }
        } else {
          setExitoso(false);
          setMensaje(data.detail || 'Error al verificar el email');
        }
      } catch (error: any) {
        setExitoso(false);
        setMensaje(
          error.response?.data?.detail ||
            'Error de conexión. Por favor intenta nuevamente.'
        );
      } finally {
        setVerificando(false);
      }
    },
    [router]
  );

  useEffect(() => {
    const token = searchParams.get('token');

    if (!token) {
      setVerificando(false);
      setMensaje('Token de verificación no encontrado');
      setExitoso(false);
      return;
    }

    verificarEmail(token);
  }, [searchParams, verificarEmail]);

  if (verificando) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">
            Verificando tu correo electrónico...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-8">
        <div className="text-center">
          {exitoso ? (
            <>
              <FaCheckCircle className="mx-auto h-16 w-16 text-green-500 mb-4" />
              <h1 className="text-2xl font-bold text-gray-900 mb-4">
                {esEmailYaVerificado
                  ? 'Email Ya Verificado'
                  : '¡Verificación Exitosa!'}
              </h1>
              <p className="text-gray-600 mb-4">{mensaje}</p>
              {email && (
                <p className="text-sm text-gray-500 mb-6">Email: {email}</p>
              )}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <FaInfoCircle className="inline text-blue-500 mr-2" />
                <span className="text-blue-700 text-sm">
                  Serás redirigido automáticamente al panel...
                </span>
              </div>
            </>
          ) : (
            <>
              <FaTimesCircle className="mx-auto h-16 w-16 text-red-500 mb-4" />
              <h1 className="text-2xl font-bold text-gray-900 mb-4">
                Error de Verificación
              </h1>
              <p className="text-gray-600 mb-6">{mensaje}</p>
            </>
          )}

          <div className="space-y-3">
            <Link
              href="/login"
              className="block w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Ir al Login
            </Link>
            <Link
              href="/"
              className="block w-full bg-gray-200 text-gray-800 py-2 px-4 rounded-lg hover:bg-gray-300 transition-colors"
            >
              Volver al Inicio
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function VerificarCorreoPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Cargando...</p>
          </div>
        </div>
      }
    >
      <VerificarCorreoContent />
    </Suspense>
  );
}
