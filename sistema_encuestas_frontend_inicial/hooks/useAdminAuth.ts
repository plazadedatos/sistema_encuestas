import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/authContext';
import { toast } from 'react-toastify';

export const useAdminAuth = () => {
  const { user, token, isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (loading) return; // Esperar a que termine de cargar

    console.log('🔐 Hook useAdminAuth - Verificando permisos...');
    console.log('Estado de autenticación:', {
      isAuthenticated,
      hasUser: !!user,
      hasToken: !!token,
      userRole: user?.rol_id,
      userEmail: user?.email,
    });

    // Si no está autenticado, redirigir a login
    if (!isAuthenticated || !user || !token) {
      console.log('❌ Usuario no autenticado, redirigiendo a login');
      toast.error('Debes iniciar sesión para acceder a esta área');
      router.push('/login');
      return;
    }

    // Si no es administrador, redirigir al panel principal
    if (user.rol_id !== 1) {
      console.log(
        `❌ Usuario ${user.email} no es administrador (rol: ${user.rol_id})`
      );
      toast.error('No tienes permisos para acceder al área de administración');
      router.push('/panel');
      return;
    }

    console.log(`✅ Acceso autorizado para administrador: ${user.email}`);
  }, [user, token, isAuthenticated, loading, router]);

  return {
    isAdmin: user?.rol_id === 1,
    user,
    token,
    loading: loading || !user || user.rol_id !== 1,
  };
};
