"use client";
import { useEffect, useState, useCallback } from "react";
import { useAuth } from "../../../context/authContext";
import api from "../../services/api";

export default function AdminRecompensasPage() {
  const { token } = useAuth();
  const [premios, setPremios] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editando, setEditando] = useState(null);
  const [mensaje, setMensaje] = useState("");
  const [error, setError] = useState("");
  
  const [form, setForm] = useState({
    nombre: "",
    descripcion: "",
    imagen_url: "",
    costo_puntos: 0,
    stock_disponible: null as number | null,
    tipo: "fisico",
    categoria: "",
    requiere_aprobacion: false,
    instrucciones_canje: "",
    terminos_condiciones: ""
  });

  const cargarPremios = useCallback(async () => {
    try {
      const res = await api.get("/premios/admin", {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPremios(res.data);
    } catch (e) {
      setError("Error al cargar premios");
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    cargarPremios();
  }, [cargarPremios]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setMensaje("");
    
    try {
      if (editando) {
        await api.put(`/premios/${editando}`, form, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setMensaje("Premio actualizado correctamente");
      } else {
        await api.post("/premios", form, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setMensaje("Premio creado correctamente");
      }
      
      cargarPremios();
      resetForm();
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Error al guardar premio");
    }
  };

  const handleEliminar = async (id: number) => {
    if (!confirm("¿Estás seguro de eliminar este premio?")) return;
    
    try {
      await api.delete(`/premios/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMensaje("Premio eliminado correctamente");
      cargarPremios();
    } catch (e) {
      setError("Error al eliminar premio");
    }
  };

  const handleEditar = (premio: any) => {
    setForm({
      nombre: premio.nombre,
      descripcion: premio.descripcion || "",
      imagen_url: premio.imagen_url || "",
      costo_puntos: Number(premio.costo_puntos) || 0,
      stock_disponible: premio.stock_disponible ? Number(premio.stock_disponible) : null,
      tipo: premio.tipo,
      categoria: premio.categoria || "",
      requiere_aprobacion: premio.requiere_aprobacion,
      instrucciones_canje: premio.instrucciones_canje || "",
      terminos_condiciones: premio.terminos_condiciones || ""
    });
    setEditando(premio.id_premio);
    setShowForm(true);
  };

  const resetForm = () => {
    setForm({
      nombre: "",
      descripcion: "",
      imagen_url: "",
      costo_puntos: 0,
      stock_disponible: null as number | null,
      tipo: "fisico",
      categoria: "",
      requiere_aprobacion: false,
      instrucciones_canje: "",
      terminos_condiciones: ""
    });
    setEditando(null);
    setShowForm(false);
  };

  if (loading) return <div className="p-8">Cargando...</div>;

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Administración de Recompensas</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          {showForm ? "Cancelar" : "Nueva Recompensa"}
        </button>
      </div>

      {mensaje && <div className="bg-green-100 text-green-700 p-4 rounded mb-4">{mensaje}</div>}
      {error && <div className="bg-red-100 text-red-700 p-4 rounded mb-4">{error}</div>}

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow mb-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block font-semibold mb-1">Nombre *</label>
              <input
                type="text"
                value={form.nombre}
                onChange={(e) => setForm({...form, nombre: e.target.value})}
                className="w-full border rounded px-3 py-2"
                required
              />
            </div>
            
            <div>
              <label className="block font-semibold mb-1">Costo en Puntos *</label>
              <input
                type="number"
                value={form.costo_puntos}
                onChange={(e) => setForm({...form, costo_puntos: parseInt(e.target.value) || 0})}
                className="w-full border rounded px-3 py-2"
                min="1"
                required
              />
            </div>

            <div>
              <label className="block font-semibold mb-1">Tipo *</label>
              <select
                value={form.tipo}
                onChange={(e) => setForm({...form, tipo: e.target.value})}
                className="w-full border rounded px-3 py-2"
              >
                <option value="fisico">Físico</option>
                <option value="digital">Digital</option>
                <option value="descuento">Descuento</option>
                <option value="servicio">Servicio</option>
              </select>
            </div>

            <div>
              <label className="block font-semibold mb-1">Stock (vacío = ilimitado)</label>
              <input
                type="number"
                value={form.stock_disponible?.toString() || ""}
                onChange={(e) => setForm({...form, stock_disponible: e.target.value ? parseInt(e.target.value) || null : null})}
                className="w-full border rounded px-3 py-2"
                min="0"
              />
            </div>

            <div className="col-span-2">
              <label className="block font-semibold mb-1">Descripción</label>
              <textarea
                value={form.descripcion}
                onChange={(e) => setForm({...form, descripcion: e.target.value})}
                className="w-full border rounded px-3 py-2"
                rows={3}
              />
            </div>

            <div className="col-span-2">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={form.requiere_aprobacion}
                  onChange={(e) => setForm({...form, requiere_aprobacion: e.target.checked})}
                  className="mr-2"
                />
                <span className="font-semibold">Requiere aprobación manual</span>
              </label>
            </div>
          </div>

          <div className="flex gap-4 mt-6">
            <button type="submit" className="bg-green-600 text-white px-6 py-2 rounded">
              {editando ? "Actualizar" : "Crear"} Premio
            </button>
            <button type="button" onClick={resetForm} className="bg-gray-400 text-white px-6 py-2 rounded">
              Cancelar
            </button>
          </div>
        </form>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {premios.map((premio) => (
          <div key={premio.id_premio} className="bg-white rounded shadow p-4">
            <h3 className="font-bold text-lg mb-2">{premio.nombre}</h3>
            <p className="text-sm text-gray-600 mb-2">{premio.descripcion}</p>
            <div className="space-y-1 text-sm">
              <p><strong>Puntos:</strong> {premio.costo_puntos}</p>
              <p><strong>Stock:</strong> {premio.stock_disponible ?? "Ilimitado"}</p>
              <p><strong>Tipo:</strong> {premio.tipo}</p>
              <p><strong>Estado:</strong> {premio.estado}</p>
            </div>
            <div className="flex gap-2 mt-4">
              <button
                onClick={() => handleEditar(premio)}
                className="bg-blue-500 text-white px-3 py-1 rounded text-sm"
              >
                Editar
              </button>
              <button
                onClick={() => handleEliminar(premio.id_premio)}
                className="bg-red-500 text-white px-3 py-1 rounded text-sm"
              >
                Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
