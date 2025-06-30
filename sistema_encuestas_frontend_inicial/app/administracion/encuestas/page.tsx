// app/administracion/encuestas/page.tsx
"use client";

import { useEffect, useRef, useState } from "react";
import Sidebar from "@/components/Sidebar";
import TopbarInterno from "@/components/TopbarInterno";
import Image from "next/image";
import axios from "axios";
import api from "@/app/services/api";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function CrearEncuestaPage() {
  const [titulo, setTitulo] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [fechaInicio, setFechaInicio] = useState("");
  const [fechaFin, setFechaFin] = useState("");
  const [visiblePara, setVisiblePara] = useState("usuarios");
  const [puntos, setPuntos] = useState<number>(0);
  const [tiempoEstimado, setTiempoEstimado] = useState("");
  const [imagen, setImagen] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [preguntas, setPreguntas] = useState<any[]>([]);
  const lastPreguntaRef = useRef<HTMLDivElement | null>(null);

  const handleAddPregunta = () => {
    setPreguntas((prev) => [
      ...prev,
      {
        texto_pregunta: "",
        tipo: "opcion_multiple",
        orden: prev.length + 1,
        opciones: [],
        abierta: true,
      },
    ]);
  };

  useEffect(() => {
    if (lastPreguntaRef.current) {
      lastPreguntaRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [preguntas.length]);

  const handlePreguntaChange = (index: number, field: string, value: any) => {
    const newPreguntas = [...preguntas];
    newPreguntas[index][field] = value;
    setPreguntas(newPreguntas);
  };

  const handleAddOpcion = (index: number) => {
    const newPreguntas = [...preguntas];
    newPreguntas[index].opciones.push({ texto_opcion: "" });
    setPreguntas(newPreguntas);
  };

  const handleOpcionChange = (pIndex: number, oIndex: number, value: string) => {
    const newPreguntas = [...preguntas];
    newPreguntas[pIndex].opciones[oIndex].texto_opcion = value;
    setPreguntas(newPreguntas);
  };

  const handleEliminarPregunta = (index: number) => {
    const nuevas = preguntas.filter((_, i) => i !== index);
    setPreguntas(nuevas);
  };

  const handleEliminarOpcion = (pIndex: number, oIndex: number) => {
    const nuevas = [...preguntas];
    nuevas[pIndex].opciones = nuevas[pIndex].opciones.filter((_: any, i: number) => i !== oIndex);
    setPreguntas(nuevas);
  };

  const togglePreguntaAbierta = (index: number) => {
    const nuevas = [...preguntas];
    nuevas[index].abierta = !nuevas[index].abierta;
    setPreguntas(nuevas);
  };

  const handleImagenChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setImagen(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async () => {
    try {
      const formData = new FormData();
      if (imagen) formData.append("imagen", imagen);
      const uploadRes = imagen
        ? await axios.post("/api/imagenes", formData)
        : { data: { url: null } };
        const payload = {
          titulo,
          descripcion,
          fecha_inicio: fechaInicio ? new Date(fechaInicio).toISOString().split("T")[0] : null,
          fecha_fin: fechaFin ? new Date(fechaFin).toISOString().split("T")[0] : null,
          estado: true,
          visible_para: visiblePara,
          imagen_url: uploadRes.data.url,
          puntos_otorga: puntos,
          tiempo_estimado: tiempoEstimado,
          preguntas,
        };



      await api.post("/api/encuestas/", payload);


      toast.success("Encuesta creada exitosamente ✅");
    } catch (err: any) {
      console.error("Error al crear encuesta", err);
      toast.error(
        err?.response?.data?.detail
          ? `Error: ${err.response.data.detail}`
          : "Ocurrió un error al crear la encuesta ❌"
      );
    }

  };

  return (
    <div className="flex ">
      <Sidebar />
      <div className="flex-1 flex flex-col h-screen overflow-y-auto bg-gray-50">
        <TopbarInterno />
        <main className="w-full max-w-3xl mx-auto px-4 py-8 space-y-6">
          <ToastContainer />
          <h1 className="text-3xl font-bold text-blue-800">Crear nueva encuesta</h1>

          <div className="space-y-4 bg-white p-6 rounded-xl shadow">
            <div>
              <label className="block text-sm font-medium mb-1">Título</label>
              <input type="text" value={titulo} onChange={(e) => setTitulo(e.target.value)} className="w-full border rounded p-2 text-sm" />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Descripción</label>
              <textarea value={descripcion} onChange={(e) => setDescripcion(e.target.value)} className="w-full border rounded p-2 text-sm" rows={3} />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Fecha de inicio</label>
                <input type="date" value={fechaInicio} onChange={(e) => setFechaInicio(e.target.value)} className="w-full border rounded p-2 text-sm" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Fecha de fin</label>
                <input type="date" value={fechaFin} onChange={(e) => setFechaFin(e.target.value)} className="w-full border rounded p-2 text-sm" />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Puntos que otorga</label>
                <input type="number" value={puntos} onChange={(e) => setPuntos(Number(e.target.value))} className="w-full border rounded p-2 text-sm" min={0} />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Tiempo estimado (ej. 5 minutos)</label>
                <input type="text" value={tiempoEstimado} onChange={(e) => setTiempoEstimado(e.target.value)} className="w-full border rounded p-2 text-sm" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Visible para</label>
              <select value={visiblePara} onChange={(e) => setVisiblePara(e.target.value)} className="w-full border rounded p-2 text-sm">
                <option value="usuarios">Usuarios</option>
                <option value="encuestadores">Encuestadores</option>
                <option value="usuarios">Usuarios</option>
                <option value="encuestadores">Encuestadores</option>

              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Imagen (opcional)</label>
              <input type="file" accept="image/*" onChange={handleImagenChange} className="w-full border rounded p-2 text-sm" />
              {preview && <Image src={preview} alt="preview" width={300} height={150} className="rounded mt-2" />}
            </div>
          </div>

          <div className="space-y-4">
            <h2 className="text-2xl font-semibold text-blue-700">Preguntas</h2>
            {preguntas.map((p, i) => (
              <div key={i} ref={i === preguntas.length - 1 ? lastPreguntaRef : null} className="bg-white border p-4 rounded shadow space-y-3">
                <div className="flex justify-between items-center">
                  <h3 className="font-medium">Pregunta {i + 1}</h3>
                  <div className="space-x-2">
                    <button
                      onClick={() => togglePreguntaAbierta(i)}
                      className="text-sm text-blue-600 hover:underline"
                    >
                      {p.abierta ? "Colapsar" : "Expandir"}
                    </button>
                    <button
                      onClick={() => handleEliminarPregunta(i)}
                      className="text-sm text-red-600 hover:underline"
                    >
                      🗑 Eliminar
                    </button>
                  </div>
                </div>

                {p.abierta && (
                  <>
                    <input
                      type="text"
                      placeholder={`Pregunta ${i + 1}`}
                      value={p.texto_pregunta}
                      onChange={(e) => handlePreguntaChange(i, "texto_pregunta", e.target.value)}
                      className="w-full border rounded p-2 text-sm"
                    />
                    <select
                      value={p.tipo}
                      onChange={(e) => handlePreguntaChange(i, "tipo", e.target.value)}
                      className="w-full border rounded p-2 text-sm"
                    >
                      <option value="opcion_multiple">Opción múltiple</option>
                      <option value="texto_libre">Texto libre</option>
                    </select>

                    {p.tipo === "opcion_multiple" && (
                      <div className="space-y-2">
                        <h4 className="font-medium">Opciones</h4>
                        {p.opciones.map((op: any, j: number) => (
                          <div key={j} className="flex items-center gap-2">
                            <input
                              type="text"
                              placeholder={`Opción ${j + 1}`}
                              value={op.texto_opcion}
                              onChange={(e) => handleOpcionChange(i, j, e.target.value)}
                              className="w-full border rounded p-2 text-sm"
                            />
                            <button
                              onClick={() => handleEliminarOpcion(i, j)}
                              className="text-red-500 text-sm"
                            >
                              ✖
                            </button>
                          </div>
                        ))}
                        <button
                          onClick={() => handleAddOpcion(i)}
                          className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 text-sm"
                        >
                          + Agregar opción
                        </button>
                      </div>
                    )}
                  </>
                )}
              </div>
            ))}
            <button
              onClick={handleAddPregunta}
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 text-sm"
            >
              + Agregar pregunta
            </button>
          </div>

          <button
            onClick={handleSubmit}
            className="w-full bg-blue-700 text-white py-3 rounded text-lg hover:bg-blue-800"
          >
            Guardar Encuesta
          </button>
        </main>
      </div>
    </div>
  );
}