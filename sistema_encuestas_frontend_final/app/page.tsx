

// app/page.tsx
export default function LoginPage() {
  return (
    <div className="min-h-screen bg-gradient-to-tr from-blue-500 to-indigo-700 flex items-center justify-center">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-sm">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">Iniciar Sesión</h1>
        <form className="space-y-5">
          <div>
            <label className="text-sm font-semibold text-gray-600 block mb-1">Correo electrónico</label>
            <input
              type="email"
              className="w-full px-4 py-2 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="tucorreo@example.com"
            />
          </div>
          <div>
            <label className="text-sm font-semibold text-gray-600 block mb-1">Contraseña</label>
            <input
              type="password"
              className="w-full px-4 py-2 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="••••••••"
            />
          </div>
          <div>
            <button
              type="button"
              className="w-full bg-blue-600 text-white py-2 rounded-xl font-semibold hover:bg-blue-700 transition-all duration-200"
            >
              Ingresar
            </button>
          </div>
        </form>
        <p className="mt-4 text-sm text-center text-gray-500">
          ¿No tienes una cuenta? <span className="text-blue-600 hover:underline cursor-pointer">Regístrate</span>
        </p>
      </div>
    </div>
  );
}
