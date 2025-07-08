"use client";

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Confetti from 'react-confetti';
import { useAuth } from '@/context/authContext';

interface WelcomeScreenProps {
  onClose: () => void;
}

export default function WelcomeScreen({ onClose }: WelcomeScreenProps) {
  const { user } = useAuth();
  const [showConfetti, setShowConfetti] = useState(true);
  const [windowDimensions, setWindowDimensions] = useState({
    width: 0,
    height: 0
  });

  useEffect(() => {
    // Obtener dimensiones de la ventana
    const handleResize = () => {
      setWindowDimensions({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };

    handleResize();
    window.addEventListener('resize', handleResize);

    // Auto cerrar después de 5 segundos
    const timer = setTimeout(() => {
      onClose();
    }, 5000);

    // Detener confeti después de 3 segundos
    const confettiTimer = setTimeout(() => {
      setShowConfetti(false);
    }, 3000);

    return () => {
      window.removeEventListener('resize', handleResize);
      clearTimeout(timer);
      clearTimeout(confettiTimer);
    };
  }, [onClose]);

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-blue-600/90 to-purple-600/90 backdrop-blur-md"
        onClick={onClose}
      >
        {showConfetti && (
          <Confetti
            width={windowDimensions.width}
            height={windowDimensions.height}
            recycle={false}
            numberOfPieces={300}
            gravity={0.2}
          />
        )}

        <motion.div
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          exit={{ scale: 0, rotate: 180 }}
          transition={{
            type: "spring",
            stiffness: 260,
            damping: 20
          }}
          className="bg-white rounded-3xl p-10 shadow-2xl max-w-md mx-auto text-center"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Avatar animado */}
          <motion.div
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="mb-6"
          >
            <div className="w-24 h-24 mx-auto bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-4xl font-bold shadow-lg">
              {user?.nombre.charAt(0).toUpperCase()}
            </div>
          </motion.div>

          {/* Mensaje de bienvenida */}
          <motion.h1
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-3xl font-bold text-gray-800 mb-2"
          >
            ¡Bienvenido de nuevo, {user?.nombre}!
          </motion.h1>

          <motion.p
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-lg text-gray-600 mb-8"
          >
            Listo para ganar puntos y responder encuestas hoy 📝✨
          </motion.p>

          {/* Estadísticas animadas */}
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="grid grid-cols-2 gap-4 mb-8"
          >
            <div className="bg-blue-50 rounded-xl p-4">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.6, type: "spring" }}
                className="text-2xl font-bold text-blue-600"
              >
                {user?.puntos_disponibles || 0}
              </motion.div>
              <p className="text-sm text-gray-600">Puntos disponibles</p>
            </div>

            <div className="bg-purple-50 rounded-xl p-4">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.7, type: "spring" }}
                className="text-2xl font-bold text-purple-600"
              >
                {user?.puntos_totales || 0}
              </motion.div>
              <p className="text-sm text-gray-600">Puntos totales</p>
            </div>
          </motion.div>

          {/* Botón de comenzar */}
          <motion.button
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.8 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onClose}
            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-full font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
          >
            Comenzar
          </motion.button>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
} 