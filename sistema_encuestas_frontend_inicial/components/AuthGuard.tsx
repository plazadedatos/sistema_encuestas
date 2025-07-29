'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../context/authContext';

export default function AuthGuard({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading, token } = useAuth();
  const router = useRouter();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    const checkAuth = () => {
      // Si no está cargando y no está autenticado, redirigir a login
      if (!loading && !isAuthenticated) {
        console.log(
          '🔒 AuthGuard: Usuario no autenticado, redirigiendo a login'
        );
        router.push('/login');
        return;
      }

      // Si no hay token, redirigir a login
      if (!loading && !token) {
        console.log('🔒 AuthGuard: No hay token, redirigiendo a login');
        router.push('/login');
        return;
      }

      // Si todo está bien, permitir acceso
      if (!loading && isAuthenticated && token) {
        setIsChecking(false);
      }
    };

    checkAuth();
  }, [isAuthenticated, loading, token, router]);

  // Mostrar loading mientras se verifica la autenticación
  if (loading || isChecking) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Verificando autenticación...</p>
        </div>
      </div>
    );
  }

  // Si no está autenticado, no mostrar nada (se está redirigiendo)
  if (!isAuthenticated || !token) {
    return null;
  }

  // Si todo está bien, mostrar el contenido
  return <>{children}</>;
}
