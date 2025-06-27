// app/login/layout.tsx (mismo para /panel/layout.tsx)
import "../globals.css"; // ✅ desde `app/panel` sube un solo nivel
import AuthGuard from "../../components/AuthGuard";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body className="bg-slate-100 min-h-screen">
        <AuthGuard>{children}</AuthGuard>
      </body>
    </html>
  );
}
