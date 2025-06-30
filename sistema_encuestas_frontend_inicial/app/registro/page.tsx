"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/app/services/api";

export default function RegistroPage() {
  const router = useRouter();

  const [form, setForm] = useState({
    nombre: "",
    apellido: "",
    documento_numero: "",
    celular_numero: "",
    email: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      const res = await api.post("/auth/registro", {
        ...form,
        rol_id: 3, // ✅ Se agrega correctamente acá
      });

      if (res.status === 200) {
        alert("Usuario registrado. Ahora podés iniciar sesión.");
        router.push("/login");
      } else {
        alert(res.data.detail || "Error en el registro");
      }
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Error de conexión con el servidor");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 bg-white p-6 rounded-xl shadow-md">
      <h2 className="text-xl font-bold mb-4 text-center">Registro de Usuario</h2>

      {(Object.keys(form) as Array<keyof typeof form>).map((campo) => (
        <input
          key={campo}
          type={campo === "password" ? "password" : "text"}
          name={campo}
          placeholder={campo.replace("_", " ")}
          value={form[campo]}
          onChange={handleChange}
          className="w-full mb-3 p-2 border border-gray-300 rounded"
        />
      ))}

      <button
        onClick={handleSubmit}
        className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition"
      >
        Registrarse
      </button>
    </div>
  );
}
