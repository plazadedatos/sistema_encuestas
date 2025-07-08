'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { FaCheckCircle, FaTimesCircle } from 'react-icons/fa';

export default function VerificarCorreoPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [verificando, setVerificando] = useState(true);
  const [mensaje, setMensaje] = useState('');
  const [exitoso, setExitoso] = useState(false);
  const [email, setEmail] = useState('');

  useEffect(() => {
    const token = searchParams.get('token');
    
    if (!token) {
      setVerificando(false);
      setMensaje('Token de verificación no encontrado');
      setExitoso(false);
      return;
    }

    verificarEmail(token);
  }, [searchParams]);

  const verificarEmail = async (token: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/verificar-correo?token=${token}`, {
        method: 'GET',
      });

      const data = await response.json();

      if (response.ok) {
        setExitoso(true);
        setMensaje(data.mensaje || 'Email verificado exitosamente');
        setEmail(data.email || '');
        
        // Redirigir al login después de 3 segundos
        setTimeout(() => {
          router.push('/login');
        }, 3000);
      } else {
        setExitoso(false);
        setMensaje(data.detail || 'Error al verificar el email');
      }
    } catch (error) {
      setExitoso(false);
      setMensaje('Error de conexión. Por favor intenta nuevamente.');
    } finally {
      setVerificando(false);
    }
  };

  if (verificando) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Verificando tu correo electrónico...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="max-w-md w-full">
        <div className="bg-white shadow-lg rounded-lg p-8">
          <div className="text-center">
            {exitoso ? (
              <>
                <FaCheckCircle className="h-16 w-16 text-green-500 mx-auto" />
                <h1 className="mt-4 text-2xl font-bold text-gray-900">
                  ¡Email Verificado!
                </h1>
                <p className="mt-2 text-gray-600">
                  {mensaje}
                </p>
                {email && (
                  <p className="mt-1 text-sm text-gray-500">
                    {email}
                  </p>
                )}
                <p className="mt-4 text-sm text-gray-600">
                  Serás redirigido al inicio de sesión en unos segundos...
                </p>
                <Link
                  href="/login"
                  className="mt-6 inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Ir al Login Ahora
                </Link>
              </>
            ) : (
              <>
                <FaTimesCircle className="h-16 w-16 text-red-500 mx-auto" />
                <h1 className="mt-4 text-2xl font-bold text-gray-900">
                  Error de Verificación
                </h1>
                <p className="mt-2 text-gray-600">
                  {mensaje}
                </p>
                <div className="mt-6 space-y-3">
                  <Link
                    href="/registro"
                    className="block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Volver al Registro
                  </Link>
                  <Link
                    href="/reenviar-verificacion"
                    className="block bg-gray-200 text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-300 transition-colors"
                  >
                    Reenviar Email de Verificación
                  </Link>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 