// components/TopbarInterno.tsx
"use client";

export default function TopbarInterno() {
  return (
    <header className="bg-white shadow px-6 py-4 flex justify-between items-center border-b">
      <h1 className="text-xl font-bold text-primary">📊 Panel de Control</h1>
      <span className="text-sm text-gray-600">👤 Usuario: admin</span>
    </header>
  );
}
