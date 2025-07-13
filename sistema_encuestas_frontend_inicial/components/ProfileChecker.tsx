"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useAuth } from "@/context/authContext";

export default function ProfileChecker() {
  const { user, token, checkProfileComplete } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [isChecking, setIsChecking] = useState(false);
  const [hasChecked, setHasChecked] = useState(false);
  const lastCheckRef = useRef<number>(0);

  useEffect(() => {
    const verifyProfile = async () => {
      // No verificar si no hay usuario o token
      if (!user || !token) return;
      
      // No verificar si ya estamos en la página de encuesta inicial
      if (pathname === '/panel/encuesta-inicial') return;
      
      // No verificar en rutas de administración
      if (pathname?.startsWith('/administracion')) return;
      
      // No verificar si ya estamos verificando
      if (isChecking) return;
      
      // No verificar si ya verificamos en esta sesión (evitar bucle)
      if (hasChecked) return;
      
      // No verificar si la última verificación fue hace menos de 5 segundos
      const now = Date.now();
      if (now - lastCheckRef.current < 5000) return;
      
      setIsChecking(true);
      lastCheckRef.current = now;
      
      try {
        console.log('🔍 Verificando estado del perfil...');
        const isProfileComplete = await checkProfileComplete();
        
        if (!isProfileComplete) {
          console.log('🔄 Perfil incompleto, redirigiendo a encuesta inicial...');
          router.push('/panel/encuesta-inicial');
        } else {
          console.log('✅ Perfil completo');
        }
        
        // Marcar como verificado para evitar verificaciones repetidas
        setHasChecked(true);
      } catch (error) {
        console.error('Error verificando perfil:', error);
        // En caso de error, asumir que está completo para no bloquear
        setHasChecked(true);
      } finally {
        setIsChecking(false);
      }
    };

    // Solo verificar si estamos en rutas del panel
    if (pathname?.startsWith('/panel') && pathname !== '/panel/encuesta-inicial') {
      verifyProfile();
    }
  }, [user, token, pathname, checkProfileComplete, router, isChecking, hasChecked]);

  // Resetear el estado cuando cambia el usuario
  useEffect(() => {
    setHasChecked(false);
    lastCheckRef.current = 0;
  }, [user?.id_usuario]);

  // Este componente no renderiza nada, solo ejecuta la lógica
  return null;
} 