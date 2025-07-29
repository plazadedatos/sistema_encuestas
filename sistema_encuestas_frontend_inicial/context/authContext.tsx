'use client';

import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
} from 'react';
import { useRouter } from 'next/navigation';
import { jwtDecode } from 'jwt-decode';
import { toast } from 'react-toastify';
import api from '@/app/services/api';
import { User, PuntosData } from '@/types';

interface JWTPayload {
  sub: string;
  usuario_id: number;
  rol_id: number;
  rol: number;
  exp?: number;
  iat?: number;
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  loading: boolean;
  showWelcome: boolean;
  setShowWelcome: (show: boolean) => void;
  login: (email: string, password: string) => Promise<boolean>;
  loginWithGoogle: (accessToken: string, userData: any) => Promise<boolean>;
  logout: () => void;
  refreshToken: () => Promise<boolean>;
  updateUser: (userData: Partial<User>) => void;
  checkProfileComplete: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showWelcome, setShowWelcome] = useState(false);

  // Función para validar si el token ha expirado
  const isTokenExpired = (token: string): boolean => {
    try {
      const decoded: any = jwtDecode(token);
      const currentTime = Date.now() / 1000;
      const isExpired = decoded.exp < currentTime;

      console.log('🔐 Validando token:', {
        exp: decoded.exp,
        currentTime,
        isExpired,
        timeUntilExpiry: decoded.exp - currentTime,
      });

      return isExpired;
    } catch (error) {
      console.error('❌ Error al decodificar token:', error);
      return true;
    }
  };

  // Función de logout mejorada (declarada antes para evitar errores)
  const logout = useCallback(() => {
    setUser(null);
    setToken(null);
    setIsAuthenticated(false);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    toast.info('Sesión cerrada correctamente.');
    router.push('/login');
  }, [router]);

  // Función para cargar usuario desde token
  const loadUserFromToken = useCallback((token: string): JWTPayload | null => {
    try {
      if (isTokenExpired(token)) {
        console.log('🔒 Token expirado, eliminando del localStorage');
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        return null;
      }

      const decoded: any = jwtDecode(token);
      console.log('🟢 Token válido cargado:', {
        email: decoded.sub,
        usuario_id: decoded.usuario_id,
        rol_id: decoded.rol_id,
        exp: new Date(decoded.exp * 1000).toLocaleString(),
      });

      return {
        ...decoded,
        rol: decoded.rol_id, // Normalizar campo
      };
    } catch (err) {
      console.error('❌ Token inválido:', err);
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      return null;
    }
  }, []);

  // Función para refrescar token (si tienes endpoint de refresh)
  const refreshToken = useCallback(async (): Promise<boolean> => {
    try {
      const response = await api.post('/auth/refresh');
      const { access_token } = response.data;

      const userData = loadUserFromToken(access_token);
      if (userData) {
        // Obtener datos completos del usuario
        const userResponse = await api.get('/usuario/me', {
          headers: { Authorization: `Bearer ${access_token}` },
        });

        setUser(userResponse.data);
        setToken(access_token);
        localStorage.setItem('token', access_token);
        localStorage.setItem('user', JSON.stringify(userResponse.data));
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error al refrescar token:', error);
      logout();
      return false;
    }
  }, [loadUserFromToken, logout]);

  // Efecto inicial para cargar usuario y token
  useEffect(() => {
    console.log('🚀 Inicializando AuthProvider...');
    const savedToken = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');

    console.log('💾 Datos guardados:', {
      hasToken: !!savedToken,
      hasUser: !!savedUser,
      tokenLength: savedToken?.length || 0,
    });

    if (savedToken && savedUser) {
      // Verificar si el token no ha expirado
      if (!isTokenExpired(savedToken)) {
        console.log('✅ Token válido, restaurando sesión');
        setToken(savedToken);
        try {
          const parsedUser = JSON.parse(savedUser);
          setUser(parsedUser);
          setIsAuthenticated(true);
          console.log('✅ Usuario restaurado:', parsedUser.email);
        } catch (error) {
          console.error('❌ Error al parsear usuario guardado:', error);
          localStorage.removeItem('user');
        }
      } else {
        // Token expirado, limpiar todo
        console.log('🔒 Token expirado al inicializar, limpiando datos');
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setToken(null);
        setUser(null);
        setIsAuthenticated(false);
      }
    } else {
      console.log('📝 No hay datos de sesión guardados');
    }
    setLoading(false);
  }, []);

  // Auto-logout cuando el token expira (verificación cada 30 segundos)
  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    if (isAuthenticated && token) {
      intervalId = setInterval(() => {
        if (isTokenExpired(token)) {
          console.log('🔒 Token expirado, cerrando sesión automáticamente');
          logout();
        }
      }, 30000); // Verificar cada 30 segundos
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [isAuthenticated, token, logout]);

  // Función de login mejorada
  const login = async (email: string, password: string): Promise<boolean> => {
    console.log('🔐 Iniciando proceso de login para:', email);
    try {
      const response = await api.post('/auth/login', { email, password });
      const { access_token } = response.data;

      console.log('✅ Token recibido del servidor');

      setToken(access_token);
      localStorage.setItem('token', access_token);

      // Obtener datos del usuario
      console.log('👤 Obteniendo datos del usuario...');
      const userResponse = await api.get('/usuario/me', {
        headers: { Authorization: `Bearer ${access_token}` },
      });

      console.log('✅ Datos del usuario obtenidos:', userResponse.data.email);

      setUser(userResponse.data);
      localStorage.setItem('user', JSON.stringify(userResponse.data));
      setIsAuthenticated(true);

      // Mostrar pantalla de bienvenida
      setShowWelcome(true);

      toast.success('¡Bienvenido! Sesión iniciada correctamente.');

      // Redirigir TODOS los usuarios a /panel
      router.push('/panel');

      return true;
    } catch (error: any) {
      console.error('❌ Error en login:', error);

      if (error.response?.status === 401) {
        toast.error('Email o contraseña incorrectos.');
      } else if (error.response?.status === 429) {
        toast.error(
          'Demasiados intentos. Espera un momento antes de intentar nuevamente.'
        );
      } else {
        toast.error('Error al iniciar sesión. Verifica tu conexión.');
      }

      return false;
    }
  };

  // Función de login con Google
  const loginWithGoogle = async (
    accessToken: string,
    userData: any
  ): Promise<boolean> => {
    console.log(
      '🔐 Iniciando proceso de login con Google para:',
      userData.email
    );
    try {
      setToken(accessToken);
      localStorage.setItem('token', accessToken);

      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      setIsAuthenticated(true);

      // Mostrar pantalla de bienvenida
      setShowWelcome(true);

      toast.success('¡Bienvenido! Sesión iniciada correctamente con Google.');

      // Redirigir TODOS los usuarios a /panel
      router.push('/panel');

      return true;
    } catch (error: any) {
      console.error('❌ Error en login con Google:', error);
      toast.error('Error al iniciar sesión con Google. Verifica tu conexión.');
      return false;
    }
  };

  // Función para actualizar datos del usuario
  const updateUser = useCallback((userData: Partial<User>) => {
    setUser(prevUser => (prevUser ? { ...prevUser, ...userData } : null));
  }, []);

  // Función para verificar si el perfil está completo
  const checkProfileComplete = useCallback(async (): Promise<boolean> => {
    if (!token) return false;

    try {
      const response = await api.get('/perfil/estado', {
        headers: { Authorization: `Bearer ${token}` },
      });

      return response.data.perfil_completo;
    } catch (error) {
      console.error('Error verificando perfil:', error);
      return true; // En caso de error, asumir que está completo para no bloquear
    }
  }, [token]);

  const contextValue: AuthContextType = {
    isAuthenticated,
    user,
    token,
    loading,
    showWelcome,
    setShowWelcome,
    login,
    loginWithGoogle,
    logout,
    refreshToken,
    updateUser,
    checkProfileComplete,
  };

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de AuthProvider');
  }
  return context;
};
