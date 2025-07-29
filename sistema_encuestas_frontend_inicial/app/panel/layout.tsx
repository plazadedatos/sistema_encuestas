// app/panel/layout.tsx
import '../globals.css';
import AuthGuard from '../../components/AuthGuard';
import Sidebar from '../../components/Sidebar';
import TopbarInterno from '../../components/TopbarInterno';
import VerificationBanner from '../../components/VerificationBanner';
import ProfileChecker from '../../components/ProfileChecker';

export default function PanelLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body className="bg-gray-50 min-h-screen">
        <AuthGuard>
          <ProfileChecker />
          <div className="flex min-h-screen">
            {/* Sidebar fijo */}
            <Sidebar />
            {/* Área principal de contenido */}
            <div className="flex flex-col flex-1 min-h-screen">
              {/* Topbar */}
              <TopbarInterno />

              {/* Contenido + banner */}
              <div className="flex-1">
                <VerificationBanner />
                <main className="p-6">{children}</main>
              </div>
            </div>
          </div>
        </AuthGuard>
      </body>
    </html>
  );
}
