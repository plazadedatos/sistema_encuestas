// app/login/layout.tsx (mismo para /panel/layout.tsx)
import "../globals.css"; // ✅ desde `app/panel` sube un solo nivel

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body className="bg-slate-100 min-h-screen">{children}</body>
    </html>
  );
}
