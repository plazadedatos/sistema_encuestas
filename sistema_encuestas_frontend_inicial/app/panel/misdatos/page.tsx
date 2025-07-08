"use client";
import { useEffect, useState } from "react";
import { getMisDatos, actualizarMisDatos } from "../../services/encuestas";
import { useAuth } from "../../../context/authContext";

export default function MisDatosPage() {
  const { token } = useAuth();
  const [datos, setDatos] = useState(null);
  const [editando, setEditando] = useState(false);
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");
  const [form, setForm] = useState({ nombre: "", apellido: "", celular_numero: "" });

  useEffect(() => {
    if (token) {
      getMisDatos(token)
        .then(res => {
          setDatos(res.data);
          setForm({
            nombre: res.data.nombre,
            apellido: res.data.apellido,
            celular_numero: res.data.celular_numero || ""
          });
        })
        .catch(() => setError("Error al cargar datos"));
    }
  }, [token]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleGuardar = async () => {
    setError("");
    setMensaje("");
    try {
      if (!token) {
        setError("No hay token de autenticación");
        return;
      }
      await actualizarMisDatos(form, token);
      setMensaje("Datos actualizados correctamente");
      setEditando(false);
      if (datos) {
        setDatos({ ...datos, ...form });
      }
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Error al actualizar datos");
    }
  };

  if (!datos) return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-blue-800 mb-2">Mis Datos</h1>
          <p className="text-gray-600">Revisa y edita la información de tu cuenta.</p>
        </div>

        {mensaje && (
          <div className="mb-6 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
            {mensaje}
          </div>
        )}
        {error && (
          <div className="mb-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Nombre</label>
            <input
              type="text"
              name="nombre"
              value={form.nombre}
              onChange={handleChange}
              disabled={!editando}
              className={`w-full px-4 py-3 border rounded-lg transition-colors ${
                editando 
                  ? 'border-blue-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200' 
                  : 'border-gray-300 bg-gray-50'
              }`}
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Apellido</label>
            <input
              type="text"
              name="apellido"
              value={form.apellido}
              onChange={handleChange}
              disabled={!editando}
              className={`w-full px-4 py-3 border rounded-lg transition-colors ${
                editando 
                  ? 'border-blue-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200' 
                  : 'border-gray-300 bg-gray-50'
              }`}
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Celular</label>
            <input
              type="text"
              name="celular_numero"
              value={form.celular_numero}
              onChange={handleChange}
              disabled={!editando}
              className={`w-full px-4 py-3 border rounded-lg transition-colors ${
                editando 
                  ? 'border-blue-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200' 
                  : 'border-gray-300 bg-gray-50'
              }`}
            />
          </div>

          <div className="flex gap-4 pt-4">
            {!editando ? (
              <button 
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
                onClick={() => setEditando(true)}
              >
                ✏️ Editar datos
              </button>
            ) : (
              <>
                <button 
                  className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors font-semibold"
                  onClick={handleGuardar}
                >
                  ✅ Guardar cambios
                </button>
                <button 
                  className="bg-gray-500 text-white px-6 py-3 rounded-lg hover:bg-gray-600 transition-colors font-semibold"
                  onClick={() => setEditando(false)}
                >
                  ❌ Cancelar
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
