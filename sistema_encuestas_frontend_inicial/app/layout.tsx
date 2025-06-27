// app/layout.tsx
import "./globals.css";
import AuthWrapper from "../components/AuthWrapper";
import { AuthProvider } from "../context/authContext";
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
