'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/app/services/api';
import Link from 'next/link';
import {
  FaUser,
  FaEnvelope,
  FaLock,
  FaIdCard,
  FaPhone,
  FaSpinner,
} from 'react-icons/fa';
import { toast } from 'react-toastify';
import GoogleLoginButton from '@/components/GoogleLoginButton';

export default function RegistroPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const [form, setForm] = useState({
    nombre: '',
    apellido: '',
    documento_numero: '',
    celular_numero: '',
    email: '',
    password: '',
  });
  const [termsAccepted, setTermsAccepted] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('🔐 Iniciando proceso de registro...');
    console.log('📋 Estado del formulario:', form);

    // Validaciones
    console.log('🔍 Verificando validaciones...');
    console.log('  - Nombre:', form.nombre, '✅' + (form.nombre ? '' : '❌'));
    console.log(
      '  - Apellido:',
      form.apellido,
      '✅' + (form.apellido ? '' : '❌')
    );
    console.log('  - Email:', form.email, '✅' + (form.email ? '' : '❌'));
    console.log(
      '  - Password:',
      form.password,
      '✅' + (form.password ? '' : '❌')
    );
    console.log(
      '  - Documento:',
      form.documento_numero,
      '✅' + (form.documento_numero ? '' : '❌')
    );

    if (
      !form.nombre ||
      !form.apellido ||
      !form.email ||
      !form.password ||
      !form.documento_numero
    ) {
      console.log('❌ Validación falló - campos obligatorios vacíos');
      toast.error('Por favor completa todos los campos obligatorios');
      return;
    }

    console.log('✅ Validación de campos obligatorios pasó');

    if (form.password.length < 6) {
      console.log('❌ Validación falló - password muy corta');
      toast.error(
        '🔒 La contraseña debe tener al menos 6 caracteres. Por favor, usa una contraseña más segura.'
      );
      return;
    }

    console.log('✅ Validación de password pasó');

    // Validar términos y condiciones
    console.log('🔍 Verificando términos y condiciones...');
    console.log(
      '  - Terms accepted:',
      termsAccepted,
      '✅' + (termsAccepted ? '' : '❌')
    );

    if (!termsAccepted) {
      console.log('❌ Validación falló - términos no aceptados');
      toast.error('Debes aceptar los términos y condiciones');
      return;
    }

    console.log('✅ Validación de términos pasó');

    setIsLoading(true);
    console.log('📤 Enviando datos de registro:', form);
    console.log(
      '🌐 URL de la API:',
      `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/registro`
    );

    try {
      console.log('🚀 Ejecutando api.post...');
      const res = await api.post('/auth/registro', form);

      console.log('✅ Respuesta del registro:', res);

      if (res.status === 200 || res.status === 201) {
        toast.success(
          '¡Registro exitoso! Revisa tu correo para verificar tu cuenta.'
        );
        // Pequeño delay para que el usuario vea el mensaje
        setTimeout(() => {
          router.push('/login');
        }, 1500);
      }
    } catch (err: any) {
      console.error('❌ Error en registro:', err);
      console.error('❌ Detalles del error:', {
        message: err.message,
        status: err.response?.status,
        data: err.response?.data,
        config: err.config,
        url: err.config?.url,
        method: err.config?.method,
      });

      const errorMessage =
        err?.response?.data?.detail ||
        'Error en el registro. Intenta nuevamente.';
      toast.error(errorMessage);
    } finally {
      console.log('🏁 Finalizando handleSubmit');
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Panel izquierdo - Imagen/Info */}
      <div className="hidden lg:block relative w-0 flex-1">
        <div className="absolute inset-0 bg-gradient-to-br from-brand-dark via-brand-vibrant to-brand-light">
          <div className="absolute inset-0 bg-black opacity-20"></div>
          <div className="absolute inset-0 flex items-center justify-center p-12">
            <div className="max-w-md text-center">
              <h3 className="text-4xl font-bold text-white mb-6">
                Únete a nuestra comunidad
              </h3>
              <p className="text-xl text-white/90 mb-8">
                Miles de usuarios ya están ganando recompensas. ¡Es tu turno!
              </p>
              <div className="space-y-4 text-left">
                <div className="flex items-center text-white/80">
                  <svg
                    className="w-6 h-6 mr-3 text-yellow-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"
                    />
                  </svg>
                  <span>Premios exclusivos para miembros</span>
                </div>
                <div className="flex items-center text-white/80">
                  <svg
                    className="w-6 h-6 mr-3 text-yellow-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <span>Sistema seguro y confiable</span>
                </div>
                <div className="flex items-center text-white/80">
                  <svg
                    className="w-6 h-6 mr-3 text-yellow-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M13 10V3L4 14h7v7l9-11h-7z"
                    />
                  </svg>
                  <span>Registro rápido y sencillo</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Panel derecho - Formulario */}
      <div className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-xl w-full space-y-8">
          {/* Logo y título */}
          <div className="text-center">
            <div className="flex justify-center mb-6">
              <div className="bg-gradient-to-r from-brand-vibrant to-brand-medium p-4 rounded-2xl shadow-lg">
                <svg
                  className="w-12 h-12 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
                  />
                </svg>
              </div>
            </div>
            <h2 className="text-3xl font-bold text-gray-900">
              Crear cuenta nueva
            </h2>
            <p className="mt-2 text-sm text-gray-600">
              Únete y comienza a ganar recompensas hoy mismo
            </p>
          </div>

          {/* Formulario */}
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <div className="space-y-4">
              {/* Fila 1: Nombre y Apellido */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label
                    htmlFor="nombre"
                    className="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Nombre *
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <FaUser className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      id="nombre"
                      name="nombre"
                      type="text"
                      required
                      value={form.nombre}
                      onChange={handleChange}
                      className="appearance-none relative block w-full pl-10 pr-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-vibrant focus:border-brand-vibrant focus:z-10 sm:text-sm transition-colors"
                      placeholder="Juan"
                      disabled={isLoading}
                    />
                  </div>
                </div>

                <div>
                  <label
                    htmlFor="apellido"
                    className="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Apellido *
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <FaUser className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      id="apellido"
                      name="apellido"
                      type="text"
                      required
                      value={form.apellido}
                      onChange={handleChange}
                      className="appearance-none relative block w-full pl-10 pr-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-vibrant focus:border-brand-vibrant focus:z-10 sm:text-sm transition-colors"
                      placeholder="Pérez"
                      disabled={isLoading}
                    />
                  </div>
                </div>
              </div>

              {/* Fila 2: Documento y Celular */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label
                    htmlFor="documento_numero"
                    className="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Número de Documento *
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <FaIdCard className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      id="documento_numero"
                      name="documento_numero"
                      type="text"
                      required
                      value={form.documento_numero}
                      onChange={handleChange}
                      className="appearance-none relative block w-full pl-10 pr-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-vibrant focus:border-brand-vibrant focus:z-10 sm:text-sm transition-colors"
                      placeholder="12345678"
                      disabled={isLoading}
                    />
                  </div>
                </div>

                <div>
                  <label
                    htmlFor="celular_numero"
                    className="block text-sm font-medium text-gray-700 mb-1"
                  >
                    Número de Celular
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <FaPhone className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      id="celular_numero"
                      name="celular_numero"
                      type="tel"
                      value={form.celular_numero}
                      onChange={handleChange}
                      className="appearance-none relative block w-full pl-10 pr-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-vibrant focus:border-brand-vibrant focus:z-10 sm:text-sm transition-colors"
                      placeholder="0981234567"
                      disabled={isLoading}
                    />
                  </div>
                </div>
              </div>

              {/* Email */}
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Correo Electrónico *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <FaEnvelope className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    value={form.email}
                    onChange={handleChange}
                    className="appearance-none relative block w-full pl-10 pr-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-vibrant focus:border-brand-vibrant focus:z-10 sm:text-sm transition-colors"
                    placeholder="tu@ejemplo.com"
                    disabled={isLoading}
                  />
                </div>
              </div>

              {/* Contraseña */}
              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Contraseña *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <FaLock className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={form.password}
                    onChange={handleChange}
                    className={`appearance-none relative block w-full pl-10 pr-10 py-3 border placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:z-10 sm:text-sm transition-colors ${
                      form.password.length > 0 && form.password.length < 6
                        ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
                        : 'border-gray-300 focus:ring-brand-vibrant focus:border-brand-vibrant'
                    }`}
                    placeholder="Mínimo 6 caracteres"
                    disabled={isLoading}
                  />
                  {form.password.length > 0 && (
                    <div className="mt-1">
                      {form.password.length < 6 ? (
                        <p className="text-sm text-red-600 flex items-center">
                          <span className="mr-1">🔒</span>
                          La contraseña debe tener al menos 6 caracteres
                        </p>
                      ) : (
                        <p className="text-sm text-green-600 flex items-center">
                          <span className="mr-1">✅</span>
                          Contraseña válida ({form.password.length} caracteres)
                        </p>
                      )}
                    </div>
                  )}
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    <svg
                      className="h-5 w-5 text-gray-400 hover:text-gray-600"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      {showPassword ? (
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                        />
                      ) : (
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                        />
                      )}
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            {/* Términos y condiciones */}
            <div className="flex items-center">
              <input
                id="terms"
                name="terms"
                type="checkbox"
                checked={termsAccepted}
                onChange={e => setTermsAccepted(e.target.checked)}
                className="h-4 w-4 text-brand-vibrant focus:ring-brand-vibrant border-gray-300 rounded"
              />
              <label
                htmlFor="terms"
                className="ml-2 block text-sm text-gray-700"
              >
                Acepto los términos y condiciones y la política de privacidad
              </label>
            </div>

            {/* Botón de registro */}
            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-brand-vibrant to-brand-medium hover:from-brand-dark hover:to-brand-vibrant focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-vibrant transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <>
                    <FaSpinner className="animate-spin mr-2" />
                    Creando cuenta...
                  </>
                ) : (
                  'Crear cuenta'
                )}
              </button>
            </div>

            {/* Separador */}
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-white text-gray-500">
                  O regístrate con
                </span>
              </div>
            </div>

            {/* Google Login */}
            <div>
              <GoogleLoginButton />
            </div>

            {/* Link de login */}
            <div className="text-center">
              <span className="text-sm text-gray-600">
                ¿Ya tienes una cuenta?{' '}
                <Link
                  href="/login"
                  className="font-medium text-brand-vibrant hover:text-brand-medium"
                >
                  Inicia sesión
                </Link>
              </span>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
